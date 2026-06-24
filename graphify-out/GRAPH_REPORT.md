# Graph Report - .  (2026-06-18)

## Corpus Check
- Corpus is ~27,811 words - fits in a single context window. You may not need a graph.

## Summary
- 606 nodes · 948 edges · 57 communities (47 shown, 10 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 216 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Orquestador Core Logic|Orquestador Core Logic]]
- [[_COMMUNITY_ActionExecutor System|ActionExecutor System]]
- [[_COMMUNITY_MCP Server & Auth|MCP Server & Auth]]
- [[_COMMUNITY_Intent Classifier|Intent Classifier]]
- [[_COMMUNITY_MCP Client Implementation|MCP Client Implementation]]
- [[_COMMUNITY_Mock MCP & Tool Tests|Mock MCP & Tool Tests]]
- [[_COMMUNITY_Vosk Wake Word|Vosk Wake Word]]
- [[_COMMUNITY_Concept Documentation|Concept Documentation]]
- [[_COMMUNITY_Conversation Memory|Conversation Memory]]
- [[_COMMUNITY_Tool Usage Tracker|Tool Usage Tracker]]
- [[_COMMUNITY_Deepgram STT Streaming|Deepgram STT Streaming]]
- [[_COMMUNITY_EventBus Implementation|EventBus Implementation]]
- [[_COMMUNITY_Interface Definitions|Interface Definitions]]
- [[_COMMUNITY_Audio Modules & VAD|Audio Modules & VAD]]
- [[_COMMUNITY_AudioProcess Pipeline|AudioProcess Pipeline]]
- [[_COMMUNITY_Audio Interfaces|Audio Interfaces]]
- [[_COMMUNITY_Main Entry Point|Main Entry Point]]
- [[_COMMUNITY_Route Client & Mock|Route Client & Mock]]
- [[_COMMUNITY_MCP Client CLI|MCP Client CLI]]
- [[_COMMUNITY_Route API Client|Route API Client]]
- [[_COMMUNITY_Groq LLM Module|Groq LLM Module]]
- [[_COMMUNITY_Movement Process|Movement Process]]
- [[_COMMUNITY_E2E Tests & Deepgram TTS|E2E Tests & Deepgram TTS]]
- [[_COMMUNITY_Porcupine Wake Word|Porcupine Wake Word]]
- [[_COMMUNITY_Local TTS Mock|Local TTS Mock]]
- [[_COMMUNITY_Provider Toggle Tests|Provider Toggle Tests]]
- [[_COMMUNITY_Groq STT Module|Groq STT Module]]
- [[_COMMUNITY_EventBus Tests|EventBus Tests]]
- [[_COMMUNITY_Audio Interface Methods|Audio Interface Methods]]
- [[_COMMUNITY_Event Consumer Tests|Event Consumer Tests]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]

## God Nodes (most connected - your core abstractions)
1. `Orquestador` - 52 edges
2. `MCPClient` - 35 edges
3. `MockMCPClient` - 30 edges
4. `EventBus` - 29 edges
5. `ConversationMemory` - 24 edges
6. `RouteClient` - 24 edges
7. `ToolUsageTracker` - 22 edges
8. `Assistant` - 21 edges
9. `query_db()` - 19 edges
10. `DeepgramSTT` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_provider_factory()` --calls--> `get_stt_provider()`  [INFERRED]
  tests/test_provider_toggle.py → src/prospectiva/main.py
- `test_e2e_mock()` --calls--> `ConfigurableClassifier`  [INFERRED]
  tests/test_e2e_mock.py → src/prospectiva/modulos/classifier/configurable_classifier.py
- `orquestador_worker()` --calls--> `RegexIntentClassifier`  [INFERRED]
  tests/test_multiprocessing_spawn.py → src/prospectiva/modulos/classifier/regex_classifier.py
- `test_e2e_mock()` --calls--> `GroqLLM`  [INFERRED]
  tests/test_e2e_mock.py → src/prospectiva/modulos/llm/groq_llm.py
- `orquestador_worker()` --calls--> `GroqLLM`  [INFERRED]
  tests/test_multiprocessing_spawn.py → src/prospectiva/modulos/llm/groq_llm.py

## Import Cycles
- None detected.

## Communities (57 total, 10 thin omitted)

### Community 0 - "Orquestador Core Logic"
Cohesion: 0.05
Nodes (22): Orquestador, _print_summary(), Print a nice summary block to the console., Core orchestrator with native tool calling, multi-turn conversation,      MCP co, Handle transcribed text., Handle direct navigation or robot commands., Handle conversational queries using Groq native tool calling.                  F, Execute tool calls and track them. (+14 more)

### Community 1 - "ActionExecutor System"
Cohesion: 0.06
Nodes (22): ActionExecutor, ActionExecutor, Registrar un handler para un intent., Ejecutar el handler para un intent., Obtener historial de acciones ejecutadas., Listar intents registrados., Ejecutor de acciones registradas por intent.          Permite registrar handlers, create_default_executor() (+14 more)

### Community 2 - "MCP Server & Auth"
Cohesion: 0.08
Nodes (39): BaseHTTPMiddleware, Request, BearerAuthMiddleware, database_summary(), find_office_by_need(), get_current_crowd_levels(), get_gates(), get_place_detail() (+31 more)

### Community 3 - "Intent Classifier"
Cohesion: 0.08
Nodes (19): ConfigurableClassifier, Classifier que carga intents desde un archivo YAML.          Permite agregar nue, Cargar configuración desde YAML., Cargar patrones por defecto., Clasificar texto usando patrones del YAML., Obtener información de un comando por su nombre., Listar todos los comandos configurados., Deterministic regex-based intent classifier for 5 intents. (+11 more)

### Community 4 - "MCP Client Implementation"
Cohesion: 0.11
Nodes (7): Exception, Any, MCPClient, MCPError, Call a tool on the MCP server., MCP JSON-RPC client for the campus information server.          Connects to a Fa, Initialize MCP connection: initialize + initialized notification.

### Community 5 - "Mock MCP & Tool Tests"
Cohesion: 0.11
Nodes (5): MCPClient, Test mock data directly., test_mock_data(), MockMCPClient, Mock MCP Client for testing without the real server.     Returns realistic ficti

### Community 6 - "Vosk Wake Word"
Cohesion: 0.07
Nodes (15): Reinicia el recognizer para una nueva sesión de escucha., Wake word detector using Vosk offline speech recognition.          NO usamos Set, VoskWakeWord, AudioPlayback, Audio playback handler., ndarray, EventBus, audio_worker() (+7 more)

### Community 7 - "Concept Documentation"
Cohesion: 0.13
Nodes (25): ActionExecutor, AudioProcess, ConfigurableClassifier, ConversationMemory, Modo Conversación, Deepgram STT (Nova-3), Deepgram TTS (Aura-2), EventBus (Cola de Eventos) (+17 more)

### Community 8 - "Conversation Memory"
Cohesion: 0.09
Nodes (12): Any, ConversationMemory, Agregar un turno al historial., Obtener historial (últimos n turnos)., Obtener historial como texto formateado para el prompt., Obtener el último turno., Obtener la última consulta del usuario., Obtener el nodo actual del robot. (+4 more)

### Community 9 - "Tool Usage Tracker"
Cohesion: 0.11
Nodes (11): Any, Test LLM tool calling with mock data., test_tool_calling(), Registrar una llamada a herramienta., Obtener todas las llamadas registradas., Obtener resumen formateado de las llamadas., Obtener lista de nombres de herramientas usadas., Número de llamadas registradas. (+3 more)

### Community 10 - "Deepgram STT Streaming"
Cohesion: 0.12
Nodes (8): DeepgramSTT, Get the latest transcription from the queue., Background thread to listen for Deepgram responses., Speech-to-Text usando Deepgram Streaming (Nova-3).          Conecta via WebSocke, Start the WebSocket connection to Deepgram., Stop the WebSocket connection., Send audio chunk to Deepgram for real-time transcription., Synchronous transcription interface.                  For Deepgram streaming, th

### Community 11 - "EventBus Implementation"
Cohesion: 0.14
Nodes (10): EventBus, Set all queues for broadcasting (called in main process)., Set the private queue for this process (called in child process)., Publish event to ALL known queues., Get next event from this process's private queue., Backward compat: access the private queue directly., Drain all pending events from all queues., Process-safe event bus. publish() broadcasts to ALL known queues.     Each proce (+2 more)

### Community 12 - "Interface Definitions"
Cohesion: 0.40
Nodes (13): ABC, IntentClassifier, SpeechToText, TextGenerator, TextToSpeech, Any, EventBus, IntentClassifier (+5 more)

### Community 13 - "Audio Modules & VAD"
Cohesion: 0.13
Nodes (8): AudioInput, Voice Activity Detection using Silero VAD., Returns True if speech detected., Audio input using sounddevice (PortAudio)., SileroVAD, SoundDeviceAudio, ndarray, VoiceActivityDetector

### Community 14 - "AudioProcess Pipeline"
Cohesion: 0.23
Nodes (6): AudioProcess, Process that handles microphone, wake word, and VAD.          State machine:, # IMPORTANT: audio is already int16 from sounddevice, do NOT multiply by 32767, Handle cooldown state: check for conversation events, then decrement counter., Abort listening and return to wake word detection., ndarray

### Community 15 - "Audio Interfaces"
Cohesion: 0.29
Nodes (7): AudioInput, VoiceActivityDetector, WakeWordDetector, AudioInput, EventBus, VoiceActivityDetector, WakeWordDetector

### Community 16 - "Main Entry Point"
Cohesion: 0.22
Nodes (12): audio_worker(), get_stt_provider(), movement_worker(), orquestador_worker(), playback_worker(), Audio playback: AUDIO_SYNTHESIZED → speaker., Movement execution: MOVEMENT_SEQUENCE_READY → execute., Create STT provider based on configuration. (+4 more)

### Community 17 - "Route Client & Mock"
Cohesion: 0.17
Nodes (7): RouteClient, Any, MockRouteClient, Cargar rutas mock predefinidas., Mock Route Client para pruebas sin el servidor real.     Devuelve rutas ficticia, Mock route calculation., Override parent __del__ to avoid httpx cleanup error.

### Community 18 - "MCP Client CLI"
Cohesion: 0.38
Nodes (3): main(), MCPClient, Any

### Community 19 - "Route API Client"
Cohesion: 0.20
Nodes (5): Any, Cliente para la API independiente de cálculo de ruta.          Recibe nombres de, Check if Route API is up., Calcular ruta entre dos nodos.                  Args:             start_node: No, RouteClient

### Community 20 - "Groq LLM Module"
Cohesion: 0.22
Nodes (5): GroqLLM, Send tool results back to the LLM to get the final response.                  Ar, Generate text with tool calling support.                  Returns dict with:, Any, TextGenerator

### Community 21 - "Movement Process"
Cohesion: 0.22
Nodes (5): MovementProcess, Ejecutar secuencia de movimientos., # TODO: Aquí se integra el código real de movimiento, Proceso que ejecuta movimientos secuenciales del robot.          Placeholder: po, EventBus

### Community 22 - "E2E Tests & Deepgram TTS"
Cohesion: 0.22
Nodes (4): Test E2E flow with mock data injected manually., test_e2e_mock(), DeepgramTTS, Deepgram Text-to-Speech using the Aura-2 model.

### Community 23 - "Porcupine Wake Word"
Cohesion: 0.25
Nodes (4): PorcupineWakeWord, Wake word detection using Porcupine (Picovoice)., Process audio chunk. Returns True if wake word detected., WakeWordDetector

### Community 24 - "Local TTS Mock"
Cohesion: 0.25
Nodes (4): TextToSpeech, LocalTTS, Placeholder for local/offline TTS.          This is a mock implementation that p, Synthesize text to speech.                  Currently returns empty bytes (mock)

### Community 25 - "Provider Toggle Tests"
Cohesion: 0.29
Nodes (6): get_tts_provider(), Create TTS provider based on configuration., Test that provider factory works correctly., Test that environment variables are set correctly., test_env_vars(), test_provider_factory()

### Community 26 - "Groq STT Module"
Cohesion: 0.29
Nodes (4): SpeechToText, GroqSTT, orquestador_worker(), Test Groq/Deepgram initialization in a spawn process.

### Community 27 - "EventBus Tests"
Cohesion: 0.29
Nodes (6): _consumer(), _publisher(), Publish 3 events to consumer queue., Consume 3 events, then publish VERIFY on ver_q., Test that EventBus works correctly across spawn processes., test_event_bus_cross_process()

### Community 28 - "Audio Interface Methods"
Cohesion: 0.33
Nodes (3): Return True if wake word detected., Return True if speech detected in chunk., ndarray

### Community 29 - "Event Consumer Tests"
Cohesion: 0.40
Nodes (4): event_consumer(), Consume events and log them., Test event consumer with real logging., test_event_consumer()

### Community 30 - "Community 30"
Cohesion: 0.40
Nodes (4): orquestador_spawn_test(), Test orquestador in spawn process., Test orquestador in spawn process., test_orquestador_spawn()

### Community 31 - "Community 31"
Cohesion: 0.40
Nodes (4): orquestador_simulator(), Simulate the Orquestador event loop., Test the full pipeline event flow., test_full_pipeline()

### Community 32 - "Community 32"
Cohesion: 0.50
Nodes (3): fs, items, payload

## Knowledge Gaps
- **8 isolated node(s):** `fs`, `items`, `payload`, `Request`, `Any` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assistant` connect `Community 33` to `Orquestador Core Logic`, `Intent Classifier`, `MCP Client Implementation`, `Mock MCP & Tool Tests`, `Vosk Wake Word`, `Deepgram STT Streaming`, `EventBus Implementation`, `Audio Modules & VAD`, `Main Entry Point`, `Route Client & Mock`, `Route API Client`, `Groq LLM Module`, `Movement Process`, `E2E Tests & Deepgram TTS`, `Local TTS Mock`, `Groq STT Module`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Why does `Orquestador` connect `Orquestador Core Logic` to `Community 33`, `MCP Client Implementation`, `Conversation Memory`, `Tool Usage Tracker`, `EventBus Implementation`, `Interface Definitions`, `Main Entry Point`, `Route API Client`, `E2E Tests & Deepgram TTS`?**
  _High betweenness centrality (0.177) - this node is a cross-community bridge._
- **Why does `RouteClient` connect `Route API Client` to `Orquestador Core Logic`, `ActionExecutor System`, `Community 33`, `Interface Definitions`, `Route Client & Mock`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Orquestador` (e.g. with `EventBus` and `IntentClassifier`) actually correct?**
  _`Orquestador` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `MCPClient` (e.g. with `Orquestador` and `Assistant`) actually correct?**
  _`MCPClient` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `MockMCPClient` (e.g. with `Assistant` and `orquestador_worker()`) actually correct?**
  _`MockMCPClient` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `EventBus` (e.g. with `AudioProcess` and `MovementProcess`) actually correct?**
  _`EventBus` has 20 INFERRED edges - model-reasoned connections that need verification._