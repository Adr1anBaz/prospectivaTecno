import os
import time
import re
import json
import logging
import traceback
from typing import Any, List, Dict

from prospectiva.bus.event_bus import EventBus
from prospectiva.interfaces.stt import SpeechToText, TextGenerator, TextToSpeech
from prospectiva.interfaces.classifier import IntentClassifier
from prospectiva.procesos.actions import create_default_executor
from prospectiva.utils.memory import ConversationMemory
from prospectiva.utils.tool_tracker import ToolUsageTracker
from prospectiva.utils.mcp_client import MCPClient
from prospectiva.utils.route_client import RouteClient

logger = logging.getLogger(__name__)

def _print_summary(title: str, lines: list[str]):
    """Print a nice summary block to the console."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)
    for line in lines:
        print(f"  • {line}")
    print("=" * 60 + "\n")

class Orquestador:
    """
    Core orchestrator with native tool calling, multi-turn conversation, 
    MCP context, and Route API.
    
    Usa Groq tool calling nativo para que el LLM decida qué herramientas
    del MCP llamar. Luego se muestran qué herramientas usó.
    """

    # Tools disponibles para el LLM (12 herramientas, ordenadas por frecuencia de uso)
    LLM_TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "search_places",
                "description": "BUSCAR LUGARES: restaurantes, laboratorios, salones, oficinas por nombre, tipo o equipamiento. Busca en ingles el equipamiento: 'projector', 'ROS', 'FPGA', 'robots', 'oscilloscope'. NO es para buscar productos en tiendas (usa search_products). NO es para buscar comida (usa search_food).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Texto a buscar: nombre, tipo, equipo (en ingles)"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "navigate_to",
                "description": "NAVEGAR hacia un lugar. Llama esta tool cuando el usuario pida ir a algun lado: 'llevame a X', 'quiero ir a X', 'navega a X', 'dirigete a X'. El destino debe ser el nombre exacto del lugar.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "destination": {"type": "string", "description": "Nombre del destino exacto (ej: Cafe Borrego, Laboratorio de Robotica, Sushi Nagoya)"}
                    },
                    "required": ["destination"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_place_detail_by_name",
                "description": "DETALLE COMPLETO de un lugar por su nombre: horarios, menu, productos, perfil, eventos.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Nombre del lugar"}
                    },
                    "required": ["name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_food",
                "description": "BUSCAR COMIDA: busca platillos en restaurantes. Ej: 'tacos', 'sushi', 'pizza', 'cafe'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Nombre del platillo o tipo de comida"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_restaurant_menu_by_name",
                "description": "MENU COMPLETO de un restaurante por su nombre exacto. Si no sabes el nombre exacto, usa search_places PRIMERO.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Nombre exacto del restaurante (ej: Sushi Nagoya, Cafe Borrego)"}
                    },
                    "required": ["name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_products",
                "description": "BUSCAR PRODUCTOS EN TIENDAS. Ej: 'calculadora', 'cuaderno', 'USB', 'pluma'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Nombre del producto"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_office_by_need",
                "description": "BUSCAR OFICINAS por profesor, departamento o servicio. Ej: 'Dr. Sanchez', 'control', 'becas'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Nombre de profesor, departamento o servicio"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_places",
                "description": "LISTAR TODOS los lugares de un tipo. Usa SOLO si el usuario pide un listado completo. Ej: 'list_places(\"restaurant\")' para todos los restaurantes. Para busquedas especificas usa search_places.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "place_type": {
                            "type": "string",
                            "description": "Tipo: restaurant, lab, store, office, classroom, gate, common_area"
                        }
                    },
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "database_summary",
                "description": "RESUMEN del campus: cuantos lugares hay de cada tipo. Solo para preguntas generales como 'que hay en el campus'.",
                "parameters": {"type": "object", "properties": {}},
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_gates",
                "description": "LISTAR puertas de acceso al campus.",
                "parameters": {"type": "object", "properties": {}},
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_crowd_levels",
                "description": "NIVELES DE AFLUENCIA actuales por lugar.",
                "parameters": {"type": "object", "properties": {}},
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_semantic_documents",
                "description": "BUSCAR DOCUMENTOS del campus por texto.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Texto a buscar"}
                    },
                    "required": ["query"]
                }
            }
        },
    ]

    def __init__(self, event_bus: EventBus, stt: SpeechToText, llm: TextGenerator,
                 tts: TextToSpeech, classifier: IntentClassifier,
                 system_prompt: str = "", mcp_client: MCPClient | None = None,
                 route_client: RouteClient | None = None, start_node: str = "base",
                 use_native_tools: bool = True):
        self.event_bus = event_bus
        self.stt = stt
        self.llm = llm
        self.tts = tts
        self.classifier = classifier
        self.system_prompt = system_prompt
        self.mcp_client = mcp_client
        self.route_client = route_client
        self.use_native_tools = use_native_tools
        self._running = True
        self._event_count = 0
        # Conversation memory
        self.memory = ConversationMemory(max_turns=20)
        self.memory.set_current_node(start_node)
        # Tool usage tracker
        self.tool_tracker = ToolUsageTracker()
        # Action executor with route client
        self.executor = create_default_executor(route_client)
        logger.info(f"[Orquestador] Registered actions: {self.executor.list_registered()}")
        logger.info(f"[Orquestador] Current node: {self.memory.get_current_node()}")
        logger.info(f"[Orquestador] Native tool calling: {use_native_tools}")
        if mcp_client:
            logger.info(f"[Orquestador] MCP client: {mcp_client.is_available()}")
        if route_client:
            logger.info(f"[Orquestador] Route client: {route_client.is_available()}")

    def run(self):
        logger.info("[Orquestador] Started")
        logger.info(f"[Orquestador] TTS available: {self.tts.is_available()}")
        while self._running:
            try:
                event = self.event_bus.get(timeout=1.0)
                if event is None:
                    continue
                event_type, payload = event
                self._event_count += 1
                logger.info(f"[Orquestador] Event #{self._event_count}: {event_type}")
                try:
                    self._handle_event(event_type, payload)
                except Exception as e:
                    logger.error(f"[Orquestador] Error handling {event_type}: {e}")
                    logger.error(traceback.format_exc())
            except Exception as e:
                logger.error(f"[Orquestador] Error in main loop: {e}")
                logger.error(traceback.format_exc())
        logger.info("[Orquestador] Stopped")

    def _handle_event(self, event_type: str, payload: Any):
        if event_type == "SPEECH_COMPLETED":
            self._handle_speech_completed(payload)
        elif event_type == "TEXT_INPUT":
            self._handle_text_input(payload)
        elif event_type == "MOVEMENT_COMPLETED":
            self._handle_movement_completed(payload)
        elif event_type == "WAKE_WORD_DETECTED":
            logger.info("[Orquestador] Wake word detected - ready for speech")
        elif event_type in (
            "AUDIO_SYNTHESIZED", "AUDIO_STREAM_START", "AUDIO_STREAM_CHUNK", "AUDIO_STREAM_END",
            "CONVERSATION_CONTINUING", "CONVERSATION_END",
            "MOVEMENT_SEQUENCE_READY",
            "STOP",
        ):
            # Events for other processes (AudioPlayback, MovementProcess, etc.)
            pass
        elif event_type == "ERROR":
            logger.error(f"[Orquestador] Error event: {payload}")
        else:
            logger.warning(f"[Orquestador] Unknown event type: {event_type}")

    def _handle_speech_completed(self, payload: dict):
        audio_bytes = payload.get("audio")
        sample_rate = payload.get("sample_rate", 16000)
        if not audio_bytes:
            logger.warning("[Orquestador] No audio bytes in SPEECH_COMPLETED")
            return
        logger.info(f"[Orquestador] Speech completed, {len(audio_bytes)} bytes, transcribing...")
        try:
            text = self.stt.transcribe(audio_bytes, sample_rate)
            logger.info(f"[Orquestador] STT raw result: '{text}'")
            # Post-process: remove consecutive repeated words/phrases
            text = self._deduplicate_repeated_words(text)
            logger.info(f"[Orquestador] STT cleaned result: '{text}'")
            # Show transcribed text prominently
            print(f"\n🎤 Transcripción: '{text}'")
            if text and text.strip():
                self._handle_text_transcribed(text.strip())
            else:
                logger.warning("[Orquestador] STT returned empty text, ignoring")
                print("⚠️ No se detectó voz clara. Repite el comando.")
                # End conversation to avoid infinite loop on noise/echo
                self.event_bus.publish("CONVERSATION_END", {})
        except Exception as e:
            logger.error(f"[Orquestador] STT error: {e}")
            logger.error(traceback.format_exc())

    def _handle_text_input(self, payload: dict):
        """Handle direct text input (from --text mode)."""
        text = payload.get("text", "").strip()
        if not text:
            logger.warning("[Orquestador] Empty TEXT_INPUT, ignoring")
            return
        logger.info(f"[Orquestador] TEXT_INPUT: '{text}'")
        print(f"\n📝 Texto recibido: '{text}'")
        self._handle_text_transcribed(text)

    def _deduplicate_repeated_words(self, text: str) -> str:
        """Remove consecutive repeated words/phrases from STT output."""
        if not text:
            return text
        import re

        text = text.strip()

        # Normalize punctuation and lowercase for comparison
        words = text.lower().split()
        if len(words) < 2:
            return text

        # Strip trailing punctuation for comparison
        def clean_word(w: str) -> str:
            return re.sub(r"[^\w\u00C0-\u017F]+", "", w)

        cleaned = [words[0]]
        for word in words[1:]:
            if clean_word(word) != clean_word(cleaned[-1]):
                cleaned.append(word)

        result = " ".join(cleaned)
        return result.strip()

    def _handle_text_transcribed(self, text: str):
        """Handle transcribed text."""
        logger.info(f"[Orquestador] Handling TEXT_TRANSCRIBED: '{text}'")
        try:
            intent, metadata = self.classifier.classify(text)
            logger.info(f"[Orquestador] Intent: {intent.value}")
            
            # Save user turn to memory
            self.memory.add_turn("user", text)
            # Clear tool tracker for new interaction
            self.tool_tracker.clear()

            if intent.value.startswith("NAVEGAR") or intent.value.startswith("COMANDO"):
                # ======== ACCIÓN DIRECTA ========
                self._handle_direct_action(text, intent)
            else:
                # ======== HABLAR → LLM CON TOOL CALLING ========
                if self.use_native_tools:
                    self._handle_conversational_with_tools(text)
                else:
                    self._handle_conversational_legacy(text)
        except Exception as e:
            logger.error(f"[Orquestador] Error in text transcription handling: {e}")
            logger.error(traceback.format_exc())

    def _handle_direct_action(self, text: str, intent):
        """Handle direct navigation or robot commands."""
        logger.info(f"[Orquestador] Action: {intent.value}")
        
        params = {"text": text, "current_node": self.memory.get_current_node()}
        result = self.executor.execute(intent.value, params)
        
        if result.get("success"):
            confirmation = self._get_confirmation(intent, result)
        else:
            confirmation = f"Error: {result.get('error', 'Unknown error')}"
        
        logger.info(f"[Orquestador] Synthesizing confirmation: '{confirmation}'")
        
        _print_summary(
            "🤖 ACCIÓN EJECUTADA",
            [
                f"Comando: '{text}'",
                f"Intent detectado: {intent.value}",
                f"Acción ejecutada: {result.get('action', 'N/A')}",
                f"Status: {result.get('status', 'N/A')}",
                f"Respuesta TTS: '{confirmation}'",
            ]
        )
        
        self.memory.add_turn("assistant", confirmation)
        self._synthesize_and_publish(confirmation)
        
        if intent.value.startswith("NAVEGAR") and result.get("movement_files"):
            end_node = result.get("node", "unknown")
            self._send_movement_sequence(result["movement_files"], end_node)

    def _handle_conversational_with_tools(self, user_text: str):
        """
        Handle conversational queries using Groq native tool calling.
        
        Flow:
        1. Send user message + tools to LLM
        2. If LLM calls tools (search_places, get_node_info):
           a. Execute tools via MCPClient
           b. Track tool usage
           c. Send results back to LLM
        3. LLM produces final response
        4. Parse final response for action/inference
        """
        logger.info("[Orquestador] Conversational mode with native tool calling...")
        
        # Build system prompt with conversation context
        system_prompt = self._build_system_prompt()
        
        # First call: LLM decides which tools to call
        try:
            first_response = self.llm.generate_with_tools(
                prompt=user_text,
                tools=self.LLM_TOOLS,
                system_prompt=system_prompt
            )
            
            logger.info(f"[Orquestador] LLM first response: finish_reason={first_response['finish_reason']}")
            
            # Si finish_reason=error sin tools: reintentar sin tools
            if first_response["finish_reason"] == "error" and not first_response["tool_calls"]:
                logger.info("[Orquestador] Tool call error, retrying without tools...")
                self._handle_without_tools(user_text, system_prompt)
                return

            # If LLM called tools, execute them
            if first_response["tool_calls"]:
                tool_results = self._execute_and_collect(first_response["tool_calls"])

                stream_fn = getattr(self.llm, 'stream_tool_results', None)
                if stream_fn:
                    logger.info("[Orquestador] Streaming final response...")
                    full_content = ""
                    for fragment in stream_fn(
                        tool_calls=first_response["tool_calls"],
                        tool_results=tool_results,
                        system_prompt=system_prompt
                    ):
                        if fragment is None:
                            break
                        full_content += fragment
                    final_response = {"content": full_content, "tool_calls": [], "finish_reason": "stop"}
                else:
                    final_response = self.llm.send_tool_results(
                        tool_calls=first_response["tool_calls"],
                        tool_results=tool_results,
                        system_prompt=system_prompt
                    )

                logger.info(f"[Orquestador] LLM final response after tools")
                self._process_llm_response(final_response, user_text, tool_calls=first_response["tool_calls"])
            else:
                # No tools called, process directly
                self._process_llm_response(first_response, user_text)
                
        except Exception as e:
            logger.error(f"[Orquestador] Tool calling error: {e}")
            # Reintentar SIN tools por si el error es del tool calling
            try:
                logger.info("[Orquestador] Retrying with simple generation (no tools)...")
                simple_prompt = self._build_system_prompt() + "\n\nUSUARIO:\n" + user_text
                buffer = ""
                for fragment in self.llm.generate(simple_prompt, ""):
                    buffer += fragment
                response_text = buffer if buffer else "No entendí bien, ¿podrías repetir?"
                self._process_llm_response({"content": response_text, "tool_calls": [], "finish_reason": "stop"}, user_text)
            except Exception as e2:
                logger.error(f"[Orquestador] Fallback also failed: {e2}")
                self._fallback_response("No entendí bien, ¿podrías repetir?", user_text)

    def _execute_and_collect(self, tool_calls: List[Dict]) -> List[Dict]:
        """Execute tools UNA VEZ y devolver resultados para el LLM."""
        logger.info(f"[Orquestador] Executing {len(tool_calls)} tool call(s)...")
        TOOL_DISPATCH = {
            "search_places": self._tool_search_places,
            "navigate_to": self._tool_navigate_to,
            "get_place_detail_by_name": self._tool_get_place_detail_by_name,
            "search_food": self._tool_search_food,
            "get_restaurant_menu_by_name": self._tool_get_restaurant_menu_by_name,
            "search_products": self._tool_search_products,
            "find_office_by_need": self._tool_find_office_by_need,
            "list_places": self._tool_list_places,
            "database_summary": self._tool_database_summary,
            "get_gates": self._tool_get_gates,
            "get_current_crowd_levels": self._tool_get_current_crowd_levels,
            "search_semantic_documents": self._tool_search_semantic_documents,
        }
        results = []
        for tc in tool_calls:
            tool_name = tc["name"]
            args = tc["arguments"]
            handler = TOOL_DISPATCH.get(tool_name)
            if handler:
                try:
                    result = handler(**(args or {}))
                except Exception as e:
                    result = {"error": str(e)}
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            results.append({
                "tool_call_id": tc["id"],
                "result": result
            })
        return results

    def _tool_health_check(self) -> dict:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.health_check()
        return {"error": "MCP client not available"}

    def _tool_database_summary(self) -> dict:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.database_summary()
        return {"error": "MCP client not available"}

    def _tool_list_places(self, place_type: str | None = None) -> list[dict]:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.list_places(place_type)
        return [{"error": "MCP client not available"}]

    def _tool_search_places(self, query: str) -> list[dict]:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.search_places(query)
        return [{"error": "MCP client not available"}]

    def _tool_get_place_detail(self, place_id: str) -> dict:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.get_place_detail(place_id)
        return {"error": "MCP client not available"}

    def _tool_get_place_detail_by_name(self, name: str) -> dict:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.get_place_detail_by_name(name)
        return {"error": "MCP client not available"}

    def _tool_search_food(self, query: str, max_price: float | None = None) -> list[dict]:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.search_food(query, max_price)
        return [{"error": "MCP client not available"}]

    def _tool_get_restaurant_menu_by_name(self, name: str) -> dict:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.get_restaurant_menu_by_name(name)
        return {"error": "MCP client not available"}

    def _tool_get_restaurant_menu(self, place_id: str) -> dict:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.get_restaurant_menu(place_id)
        return {"error": "MCP client not available"}

    def _tool_search_products(self, query: str, max_price: float | None = None) -> list[dict]:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.search_products(query, max_price)
        return [{"error": "MCP client not available"}]

    def _tool_get_store_products(self, place_id: str) -> list[dict]:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.get_store_products(place_id)
        return [{"error": "MCP client not available"}]

    def _tool_find_office_by_need(self, query: str) -> list[dict]:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.find_office_by_need(query)
        return [{"error": "MCP client not available"}]

    def _tool_get_gates(self) -> list[dict]:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.get_gates()
        return [{"error": "MCP client not available"}]

    def _tool_get_current_crowd_levels(self) -> list[dict]:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.get_current_crowd_levels()
        return [{"error": "MCP client not available"}]

    def _tool_search_semantic_documents(self, query: str) -> list[dict]:
        if self.mcp_client and self.mcp_client.is_available():
            return self.mcp_client.search_semantic_documents(query)
        return [{"error": "MCP client not available"}]

    def _tool_navigate_to(self, destination: str) -> dict:
        if not self.route_client or not self.route_client.is_available():
            return {"error": "Route API no disponible", "success": False}
        current = self.memory.get_current_node()
        logger.info(f"[Orquestador] Navigate: {current} -> {destination}")

        # Si current y destination son iguales, ya estamos ahi
        if current.lower() == destination.lower():
            return {
                "success": True,
                "destination": destination,
                "from": current,
                "response": f"Ya estas en {destination}.",
                "distance_m": 0,
                "estimated_time": 0,
            }

        result = self.route_client.calculate_route(current, destination)
        if result.get("success"):
            movement_files = result.get("movement_files") or result.get("route_files") or []
            dist = result.get("total_distance_m", 0)
            has_real_files = any(f and f.endswith('.csv') for f in movement_files)

            if not has_real_files and dist == 0:
                return {
                    "success": True,
                    "destination": destination,
                    "from": current,
                    "response": f"Ya estas en {destination}.",
                    "distance_m": 0,
                    "estimated_time": 0,
                }
            if not has_real_files:
                self.memory.set_current_node(destination)
                return {
                    "success": True,
                    "destination": destination,
                    "from": current,
                    "response": f"Ruta calculada a {destination}. Son {dist} metros.",
                    "distance_m": dist,
                    "estimated_time": result.get("estimated_time", 0),
                    "note": "Sin archivos CSV de moviemiento, solo ruta teorica.",
                }

            self.memory.set_current_node(destination)
            self._send_movement_sequence(movement_files, destination)
            return {
                "success": True,
                "destination": destination,
                "from": current,
                "response": f"Voy a {destination}. Son {dist} metros, aproximadamente {result.get('estimated_time', 0)} segundos.",
                "distance_m": dist,
                "estimated_time": result.get("estimated_time", 0),
            }
        return {
            "success": False,
            "error": result.get("error", f"No se pudo calcular la ruta a '{destination}'"),
        }

    def _build_system_prompt(self) -> str:
        """Build system prompt with context and history."""
        parts = [
            "Eres un asistente de información universitaria. Hablas español.",
            "",
            "DATOS DISPONIBLES EN EL CAMPUS:",
            "Restaurantes (9): Tacos Don Julio, Sushi Nagoya, Dragon Dorado, Cafe Borrego, La Bella Italia, Green Bowl, El Rincon del Sabor, Subway Campus, Giornale",
            "Tiendas: Papeleria Campus (cuadernos, calculadoras, plumas), Tienda de Conveniencia (snacks, bebidas, cargadores)",
            "Oficinas: Dr. Sanchez, Dra. Gonzalez, Dr. Mendoza, etc.",
            "Laboratorios: Robotica (ROS), Circuitos (FPGA), Control (projector, plantas, motores)",
            "Equipamiento en laboratorios (buscar en INGLES con terminos SIMPLES): 'projector' (proyector), 'ROS', 'FPGA', 'oscilloscope', 'robots'",
            "Cuando busques equipamiento, NO combines palabras. Busca terminos individuales: 'projector' para proyector, 'robots' para robotica.",
            "Puertas: Puerta 10 (principal)",
            "",
            "GUIA DE HERRAMIENTAS:",
            "- PRODUCTOS de tienda (calculadora, cuaderno, USB) -> search_products",
            "- COMIDA/platillos (tacos, sushi, pizza) -> search_food",
            "- MENU de un restaurante (nombre exacto) -> get_restaurant_menu_by_name",
            "- Si falla el nombre exacto, busca el lugar con search_places PRIMERO",
            "- NAVEGAR a un lugar (llevame a X, quiero ir a X) -> navigate_to",
            "- LUGARES (restaurantes, laboratorios, salones) -> search_places",
            "- OFICINAS de profesores/departamentos -> find_office_by_need",
            "- DETALLE + horarios de un lugar -> get_place_detail_by_name",
            "- PUERTAS de acceso -> get_gates",
            "- DOCUMENTOS del campus -> search_semantic_documents",
            "- AFLUENCIA actual -> get_current_crowd_levels",
            "",
            "REGLAS:",
            "- Cuando el usuario pregunte por algo, USA SIEMPRE las herramientas primero",
            "- Si un tool falla porque el nombre no es exacto, usa search_places para encontrar el nombre correcto y vuelve a intentar",
            "- No inventes nombres de restaurantes o productos; busca siempre en la BD",
            "- NUNCA uses sintaxis '<function=...>' ni '<...>' en tus respuestas. Responde solo como texto natural.",
            "- Cuando navigate_to devuelva success=true y 'distance_m' sea 0, significa que YA estas en ese lugar. Di 'Ya estas ahi.'",
            "- Cuando navigate_to devuelva success=true y un campo 'response', USA ese texto como tu respuesta directa.",
            "- Cuando navigate_to falle porque el destino no existe en la BD, usa search_places PRIMERO para encontrar el nombre exacto, luego llama navigate_to de nuevo.",
            "- Ejemplo: si navigate_to('salon L') falla, busca con search_places('salon L') para obtener el nombre real, luego navigate_to('Salon A-201').",
            "- Si no tienes suficiente información, haz máximo 1 pregunta de seguimiento",
            "- Máximo 1 oracion en tu respuesta. Responde directo y sin rodeos.",
            "- Responde de forma natural y útil en español",
            "",
            f"UBICACIÓN ACTUAL DEL ROBOT: {self.memory.get_current_node()}",
            "",
        ]
        
        history = self.memory.get_formatted_history()
        if history:
            parts.append("HISTORIAL DE CONVERSACIÓN:")
            parts.append(history)
            parts.append("")
        
        return "\n".join(parts)

    def _process_llm_response(self, response: Dict, user_text: str, tool_calls: list | None = None):
        """Process LLM response (after tool calling or direct)."""
        content = self._clean_response(response.get("content", "") or "")
        
        # Try to parse JSON from content
        parsed = self._parse_llm_json(content)
        
        if parsed:
            response_text = parsed.get("response", content)
            action = parsed.get("action", "none")
            params = parsed.get("params", {})
            end_node = params.get("end_node", "")
            confidence = parsed.get("confidence", 0.0)
            need_more_info = parsed.get("need_more_info", False)
        else:
            # Use content as response text
            response_text = content
            action = "none"
            end_node = ""
            confidence = 0.0
            need_more_info = False
        
        logger.info(f"[Orquestador] LLM: action={action}, end_node={end_node}, confidence={confidence:.2f}")
        
        # Save to memory
        self.memory.add_turn("assistant", response_text, {
            "action": action,
            "confidence": confidence,
            "end_node": end_node,
        })
        
        # Print tool usage summary
        if self.tool_tracker.count() > 0:
            print(self.tool_tracker.get_summary())
        
        # Print response summary
        if action == "infer_destination" and end_node:
            _print_summary(
                "🧠 INFERENCIA DE DESTINO",
                [
                    f"Consulta: '{user_text}'",
                    f"Respuesta: '{response_text}'",
                    f"Destino inferido: {end_node}",
                    f"Confianza: {confidence:.2f}",
                    f"Herramientas usadas: {self.tool_tracker.count()}",
                ]
            )
            self._handle_inferred_destination(end_node, response_text)
        else:
            _print_summary(
                "🧠 RESPUESTA CONVERSACIONAL",
                [
                    f"Consulta: '{user_text}'",
                    f"Respuesta: '{response_text}'",
                    f"Necesita más info: {need_more_info}",
                    f"Herramientas usadas: {self.tool_tracker.count()}",
                ]
            )
            self._synthesize_and_publish(response_text)
            # Signal AudioProcess to stay in listening mode for natural conversation
            self._publish_conversation_continuing(response_text, tool_calls=tool_calls)

    def _handle_conversational_legacy(self, user_text: str):
        """Legacy conversational mode without tool calling (fallback)."""
        logger.info("[Orquestador] Conversational mode (legacy)...")
        
        mcp_context = ""
        if self.mcp_client and self.mcp_client.is_available():
            mcp_context = self.mcp_client.get_context_for_query(user_text)
        
        history = self.memory.get_formatted_history()
        prompt = self._build_legacy_prompt(user_text, mcp_context, history)
        
        try:
            buffer = ""
            for fragment in self.llm.generate(prompt, self.system_prompt):
                buffer += fragment
            
            parsed = self._parse_llm_json(buffer)
            if parsed:
                self._process_llm_response_legacy(parsed, user_text)
            else:
                self._fallback_response(buffer, user_text)
        except Exception as e:
            logger.error(f"[Orquestador] LLM error: {e}")
            self._fallback_response("No entendí bien, ¿podrías repetir?", user_text)

    def _build_legacy_prompt(self, user_text: str, mcp_context: str, history: str) -> str:
        """Build legacy prompt without tool calling."""
        prompt_parts = [
            "Eres un asistente de navegación universitario. Hablas español. Responde en formato JSON.",
            "",
            "REGLAS:",
            "- Si el usuario pide un lugar específico → action='infer_destination'",
            "- Si el usuario es vago, haz preguntas de seguimiento",
            "- Máximo 2 preguntas de seguimiento",
            "- Cuando confianza >= 0.8, infiere el destino",
            "- end_node debe ser el nombre del nodo en el sistema",
            "- Máximo 1 oración en 'response'",
            "",
        ]
        
        if mcp_context:
            prompt_parts.append("CONTEXTO UNIVERSITARIO:")
            prompt_parts.append(mcp_context)
            prompt_parts.append("")
        
        if history:
            prompt_parts.append("HISTORIAL:")
            prompt_parts.append(history)
            prompt_parts.append("")
        
        prompt_parts.append(f"TU POSICIÓN: {self.memory.get_current_node()}")
        prompt_parts.append("")
        prompt_parts.append("USUARIO:")
        prompt_parts.append(user_text)
        prompt_parts.append("")
        prompt_parts.append("Responde con JSON:")
        prompt_parts.append(json.dumps({
            "response": "tu respuesta",
            "action": "none",
            "params": {"end_node": "nombre"},
            "confidence": 0.95,
            "need_more_info": False
        }, indent=2, ensure_ascii=False))
        
        return "\n".join(prompt_parts)

    def _process_llm_response_legacy(self, parsed: dict, user_text: str):
        """Process legacy LLM response."""
        response_text = parsed.get("response", "No entendí bien.")
        action = parsed.get("action", "none")
        params = parsed.get("params", {})
        end_node = params.get("end_node", "")
        
        self.memory.add_turn("assistant", response_text, {
            "action": action,
            "end_node": end_node,
        })
        
        if action == "infer_destination" and end_node:
            self._handle_inferred_destination(end_node, response_text)
        else:
            self._synthesize_and_publish(response_text)

    def _clean_response(self, text: str) -> str:
        """Remove raw function call syntax the LLM might leak."""
        if not text:
            return text
        text = re.sub(r'<function=\w+>.*?</function>', '', text, flags=re.DOTALL)
        text = re.sub(r'<function=\w+>', '', text)
        text = re.sub(r'</function>', '', text)
        text = re.sub(r'\[function=\w+\].*?\[/function\]', '', text, flags=re.DOTALL)
        text = text.strip()
        return text if text else "No tengo esa información disponible."

    def _handle_without_tools(self, user_text: str, system_prompt: str):
        """Responder sin tools cuando el tool calling falla."""
        try:
            prompt = system_prompt + "\n\nUSUARIO:\n" + user_text
            buffer = ""
            for fragment in self.llm.generate(prompt, ""):
                buffer += fragment
            if buffer:
                self._process_llm_response(
                    {"content": self._clean_response(buffer), "tool_calls": [], "finish_reason": "stop"},
                    user_text
                )
            else:
                self._fallback_response("No entendí bien, ¿podrías repetir?", user_text)
        except Exception as e:
            logger.error(f"[Orquestador] Without-tools fallback failed: {e}")
            self._fallback_response("No entendí bien, ¿podrías repetir?", user_text)

    def _parse_llm_json(self, buffer: str) -> dict | None:
        """Extract and parse JSON from LLM response."""
        try:
            json_match = re.search(r'\{.*\}', buffer, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        return None

    def _handle_inferred_destination(self, end_node: str, response_text: str):
        """Handle inferred destination."""
        current_node = self.memory.get_current_node()
        logger.info(f"[Orquestador] Inferring: {current_node} → {end_node}")
        
        if self.route_client and self.route_client.is_available():
            route_result = self.route_client.calculate_route(current_node, end_node)
            
            if route_result.get("success"):
                movement_files = route_result.get("movement_files", [])
                estimated_time = route_result.get("estimated_time", 0)
                
                self.memory.set_current_node(end_node)
                
                if movement_files:
                    self._send_movement_sequence(movement_files, end_node)
                
                tts_text = f"{response_text} Voy al {end_node}."
                self._synthesize_and_publish(tts_text)
                
                _print_summary(
                    "🗺️ RUTA CALCULADA",
                    [
                        f"Inicio: {current_node}",
                        f"Destino: {end_node}",
                        f"Archivos: {len(movement_files)}",
                        f"Tiempo estimado: {estimated_time}s",
                    ]
                )
            else:
                self._synthesize_and_publish(f"{response_text} No pude calcular la ruta.")
        else:
            logger.warning("[Orquestador] Route API unavailable")
            self.memory.set_current_node(end_node)
            self._synthesize_and_publish(response_text)

    def _send_movement_sequence(self, files: list[str], end_node: str):
        """Send movement sequence to MovementProcess."""
        logger.info(f"[Orquestador] Publishing MOVEMENT_SEQUENCE_READY: {len(files)} files → {end_node}")
        self.event_bus.publish("MOVEMENT_SEQUENCE_READY", {
            "movement_files": files,
            "end_node": end_node,
        })

    def _handle_movement_completed(self, payload: dict):
        """Handle movement completion."""
        end_node = payload.get("end_node", "unknown")
        logger.info(f"[Orquestador] Movement completed. Arrived at: {end_node}")
        self.memory.set_current_node(end_node)

    def _synthesize_and_publish(self, text: str):
        """Synthesize text and publish audio (streaming si el TTS lo soporta)."""
        try:
            if hasattr(self.tts, 'synthesize_stream'):
                logger.info(f"[Orquestador] Streaming TTS: '{text[:80]}...'")
                stream = self.tts.synthesize_stream(text)
                header = b""
                sent_start = False
                for i, chunk in enumerate(stream):
                    if not chunk:
                        continue
                    if i == 0 and len(chunk) > 44:
                        # Primera llamada tiene el WAV header + data
                        header = chunk[:44]
                        data = chunk[44:]
                        self.event_bus.publish("AUDIO_STREAM_START", {"header": header})
                        if data:
                            self.event_bus.publish("AUDIO_STREAM_CHUNK", {"chunk": data})
                        sent_start = True
                    elif i == 0:
                        header = chunk
                        self.event_bus.publish("AUDIO_STREAM_START", {"header": header})
                        sent_start = True
                    else:
                        self.event_bus.publish("AUDIO_STREAM_CHUNK", {"chunk": chunk})
                if sent_start:
                    self.event_bus.publish("AUDIO_STREAM_END", {})
                return

            # Legacy: full audio
            audio_bytes = self.tts.synthesize(text)
            if audio_bytes:
                self.event_bus.publish("AUDIO_SYNTHESIZED", {"audio": audio_bytes})
        except Exception as e:
            logger.error(f"[Orquestador] TTS error: {e}")
            logger.error(traceback.format_exc())

    RESOLUTIVE_TOOLS = {"navigate_to", "list_places", "get_gates", "database_summary"}

    def _publish_conversation_continuing(self, response_text: str, tool_calls: list | None = None):
        """
        Signal AudioProcess to stay in listening mode for natural conversation.
        Publishes CONVERSATION_CONTINUING unless the response indicates conversation end
        or a resolutive tool was called (navigate, list, etc.).
        """
        # If LLM called a resolutive tool (navigation, listing), end conversation
        if tool_calls:
            called_names = {tc.get("name", "") for tc in tool_calls if isinstance(tc, dict)}
            if called_names & self.RESOLUTIVE_TOOLS:
                self.event_bus.publish("CONVERSATION_END", {})
                logger.info(f"[Orquestador] Conversation ended — resolutive tool(s) called: {called_names}")
                return

        end_phrases = ["adiós", "adios", "hasta luego", "chao", "bye", "nos vemos",
                       "eso es todo", "gracias por nada", "ya no necesito"]
        text_lower = response_text.lower()
        if any(phrase in text_lower for phrase in end_phrases):
            self.event_bus.publish("CONVERSATION_END", {})
            logger.info("[Orquestador] Conversation ended by assistant response")
        else:
            self.event_bus.publish("CONVERSATION_CONTINUING", {})
            logger.info("[Orquestador] Conversation continuing — AudioProcess stays in listening mode")

    def _fallback_response(self, text: str, user_text: str):
        """Fallback when LLM doesn't return valid response."""
        logger.warning(f"[Orquestador] Fallback: '{text[:80]}...'")
        self.memory.add_turn("assistant", text, {"fallback": True})
        
        _print_summary(
            "⚠️ RESPUESTA FALLBACK",
            [
                f"Consulta: '{user_text}'",
                f"Respuesta: '{text[:80]}...'",
            ]
        )
        
        self._synthesize_and_publish(text)
        self._publish_conversation_continuing(text)

    def _get_confirmation(self, intent, result: dict) -> str:
        """Generate confirmation text."""
        if result.get("name"):
            return f"Voy a {result['name']}."
        
        confirmations = {
            "NAVEGAR_GIORNALE": "Voy al edificio Giornale.",
            "NAVEGAR_BIOMEDICA": "Voy al edificio de Biomédica.",
            "NAVEGAR_BIBLIOTECA": "Voy a la Biblioteca Central.",
            "NAVEGAR_CAFETERIA": "Voy a la cafetería.",
            "COMANDO_SIT": "Me siento.",
            "COMANDO_DANCE": "¡Bailando!",
            "COMANDO_STAND": "Me pongo de pie.",
            "COMANDO_WAVE": "¡Hola!",
            "COMANDO_WALK": "Caminando.",
            "COMANDO_STOP": "Detenido.",
        }
        return confirmations.get(intent.value, "Entendido.")

    def stop(self):
        self._running = False
