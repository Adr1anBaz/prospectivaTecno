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

    # Tools disponibles para el LLM (MCP server)
    LLM_TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "health_check",
                "description": "Check that the MCP server can connect to the database",
                "parameters": {"type": "object", "properties": {}},
            }
        },
        {
            "type": "function",
            "function": {
                "name": "database_summary",
                "description": "Return a quick summary of the database: total places and count by type",
                "parameters": {"type": "object", "properties": {}},
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_places",
                "description": "List campus places. Optionally filter by type: restaurant, classroom, lab, store, office, department, gate, common_area",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "place_type": {
                            "type": "string",
                            "description": "Optional filter: restaurant, classroom, lab, store, office, department, gate, common_area"
                        }
                    },
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_places",
                "description": "Search places by name, description, type, room code, building name or metadata",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query text"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_place_detail",
                "description": "Get detailed information about a place using its place_id (UUID). Includes opening hours and type-specific profile",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "place_id": {"type": "string", "description": "UUID of the place"}
                    },
                    "required": ["place_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_place_detail_by_name",
                "description": "Get detailed information about a place using its name (useful when the user does not know the UUID)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Place name to search"}
                    },
                    "required": ["name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_food",
                "description": "Search restaurant menu items by name, description, category or dietary tags. Optionally filter by max price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Food search query"},
                        "max_price": {"type": "number", "description": "Optional maximum price filter"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_restaurant_menu_by_name",
                "description": "Get restaurant menu using the restaurant name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Restaurant name"}
                    },
                    "required": ["name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_restaurant_menu",
                "description": "Get menus and menu items for a restaurant using its place_id (UUID). Use get_place_detail_by_name first to find the ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "place_id": {"type": "string", "description": "UUID of the restaurant place"}
                    },
                    "required": ["place_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_products",
                "description": "Search store products by name, description or category. Optionally filter by max price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Product search query"},
                        "max_price": {"type": "number", "description": "Optional maximum price filter"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_store_products",
                "description": "Get products for a store using its place_id (UUID)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "place_id": {"type": "string", "description": "UUID of the store place"}
                    },
                    "required": ["place_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_office_by_need",
                "description": "Search offices/departments by purpose, department type or services",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for office purpose, department type or services"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_gates",
                "description": "List campus gates with entry/exit permissions and adjacent streets",
                "parameters": {"type": "object", "properties": {}},
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_crowd_levels",
                "description": "Get latest crowd level per place when available",
                "parameters": {"type": "object", "properties": {}},
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_semantic_documents",
                "description": "Search semantic documents by text (temporary lexical search, later vector search)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Document search query"}
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
        elif event_type in ("AUDIO_SYNTHESIZED", "CONVERSATION_CONTINUING", "CONVERSATION_END", "STOP"):
            # AudioPlayback handles AUDIO_SYNTHESIZED; AudioProcess/TextInputProcess handle conversation events
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

        # Normalize punctuation and lowercase for comparison
        words = text.lower().split()
        if len(words) < 2:
            return text.strip()

        # Strip trailing punctuation for comparison
        def clean_word(w: str) -> str:
            return re.sub(r"[^\w\u00C0-\u017F]+", "", w)

        cleaned = [words[0]]
        for word in words[1:]:
            if clean_word(word) != clean_word(cleaned[-1]):
                cleaned.append(word)

        result = " ".join(cleaned)
        # Preserve original capitalization of first letter
        if text and result:
            result = text[0] + result[1:]
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
            
            # If LLM called tools, execute them
            if first_response["tool_calls"]:
                self._execute_tool_calls(first_response["tool_calls"])
                
                # Second call: send tool results back to LLM
                tool_results = self._prepare_tool_results(first_response["tool_calls"])
                final_response = self.llm.send_tool_results(
                    tool_calls=first_response["tool_calls"],
                    tool_results=tool_results,
                    system_prompt=system_prompt
                )
                
                logger.info(f"[Orquestador] LLM final response after tools")
                self._process_llm_response(final_response, user_text)
            else:
                # No tools called, process directly
                self._process_llm_response(first_response, user_text)
                
        except Exception as e:
            logger.error(f"[Orquestador] Tool calling error: {e}")
            logger.error(traceback.format_exc())
            self._fallback_response("No entendí bien, ¿podrías repetir?", user_text)

    def _execute_tool_calls(self, tool_calls: List[Dict]):
        """Execute tool calls and track them."""
        logger.info(f"[Orquestador] Executing {len(tool_calls)} tool call(s)...")

        TOOL_DISPATCH = {
            "health_check": self._tool_health_check,
            "database_summary": self._tool_database_summary,
            "list_places": self._tool_list_places,
            "search_places": self._tool_search_places,
            "get_place_detail": self._tool_get_place_detail,
            "get_place_detail_by_name": self._tool_get_place_detail_by_name,
            "search_food": self._tool_search_food,
            "get_restaurant_menu_by_name": self._tool_get_restaurant_menu_by_name,
            "get_restaurant_menu": self._tool_get_restaurant_menu,
            "search_products": self._tool_search_products,
            "get_store_products": self._tool_get_store_products,
            "find_office_by_need": self._tool_find_office_by_need,
            "get_gates": self._tool_get_gates,
            "get_current_crowd_levels": self._tool_get_current_crowd_levels,
            "search_semantic_documents": self._tool_search_semantic_documents,
        }

        for tc in tool_calls:
            tool_name = tc["name"]
            args = tc["arguments"]
            start_time = time.time()
            handler = TOOL_DISPATCH.get(tool_name)
            if handler:
                try:
                    result = handler(**(args or {}))
                except Exception as e:
                    result = {"error": str(e)}
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            duration = (time.time() - start_time) * 1000
            self.tool_tracker.record(tool_name, args, result, duration)
            logger.info(f"[Orquestador] Tool {tool_name} executed in {duration:.0f}ms")

    def _prepare_tool_results(self, tool_calls: List[Dict]) -> List[Dict]:
        """Prepare tool results for sending back to LLM."""
        TOOL_DISPATCH = {
            "health_check": self._tool_health_check,
            "database_summary": self._tool_database_summary,
            "list_places": self._tool_list_places,
            "search_places": self._tool_search_places,
            "get_place_detail": self._tool_get_place_detail,
            "get_place_detail_by_name": self._tool_get_place_detail_by_name,
            "search_food": self._tool_search_food,
            "get_restaurant_menu_by_name": self._tool_get_restaurant_menu_by_name,
            "get_restaurant_menu": self._tool_get_restaurant_menu,
            "search_products": self._tool_search_products,
            "get_store_products": self._tool_get_store_products,
            "find_office_by_need": self._tool_find_office_by_need,
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

    def _build_system_prompt(self) -> str:
        """Build system prompt with context and history."""
        parts = [
            "Eres un asistente de información universitaria. Hablas español.",
            "",
            "INFORMACIÓN DEL CAMPUS DISPONIBLE:",
            "- search_places(query): busca lugares por nombre, descripción, tipo o edificio",
            "- get_place_detail_by_name(name): obtén horarios, menús, productos de un lugar",
            "- search_food(query, max_price?): busca platillos por nombre, descripción o precio",
            "- get_restaurant_menu_by_name(name): obtén el menú completo de un restaurante",
            "- search_products(query, max_price?): busca productos en tiendas",
            "- find_office_by_need(query): busca oficinas/departamentos por servicio",
            "- get_gates(): lista las puertas de acceso al campus",
            "- get_current_crowd_levels(): niveles de afluencia actual",
            "- search_semantic_documents(query): busca documentos del campus",
            "",
            "REGLAS:",
            "- Cuando el usuario pregunte por lugares, comida, horarios, usa las herramientas",
            "- Si el usuario pide un lugar específico, infiere el destino",
            "- Si no tienes suficiente información, haz preguntas de seguimiento",
            "- Máximo 2 preguntas de seguimiento",
            "- Máximo 1 oración en tu respuesta",
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

    def _process_llm_response(self, response: Dict, user_text: str):
        """Process LLM response (after tool calling or direct)."""
        content = response.get("content", "No entendí bien.")
        
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
            self._publish_conversation_continuing(response_text)

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
        """Synthesize text and publish AUDIO_SYNTHESIZED."""
        try:
            logger.info(f"[Orquestador] Synthesizing: '{text[:80]}...'")
            audio_bytes = self.tts.synthesize(text)
            if audio_bytes:
                logger.info(f"[Orquestador] Publishing AUDIO_SYNTHESIZED ({len(audio_bytes)} bytes)")
                self.event_bus.publish("AUDIO_SYNTHESIZED", {"audio": audio_bytes})
            else:
                logger.warning("[Orquestador] TTS returned empty audio")
        except Exception as e:
            logger.error(f"[Orquestador] TTS error: {e}")
            logger.error(traceback.format_exc())

    def _publish_conversation_continuing(self, response_text: str):
        """
        Signal AudioProcess to stay in listening mode for natural conversation.
        Publishes CONVERSATION_CONTINUING unless the response indicates conversation end.
        """
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
