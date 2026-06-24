import os
import sys
import time
import logging
import multiprocessing as mp
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from prospectiva.bus.event_bus import EventBus

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Load .env
load_dotenv()

# System prompt for university context
SYSTEM_PROMPT = """Eres un asistente de navegación universitario. Hablas español."""

# ---------------------------------------------------------------------------
# Provider Factory
# ---------------------------------------------------------------------------

def get_stt_provider(groq_key: str, deepgram_key: str, provider: str = "groq"):
    """Create STT provider based on configuration."""
    if provider == "deepgram":
        logger.info("🎙️ STT Provider: Deepgram (Nova-3 streaming)")
        from prospectiva.modulos.stt.deepgram_stt import DeepgramSTT
        return DeepgramSTT(api_key=deepgram_key, model="nova-3", language="es")
    elif provider == "googlecloud":
        logger.info("🎙️ STT Provider: Google Cloud Speech-to-Text")
        from prospectiva.modulos.stt.google_stt import GoogleCloudSTT
        return GoogleCloudSTT()
    else:
        logger.info("🎙️ STT Provider: Groq (Whisper)")
        from prospectiva.modulos.stt.groq_stt import GroqSTT
        return GroqSTT(api_key=groq_key, model="whisper-large-v3-turbo")


def get_tts_provider(deepgram_key: str, provider: str = "deepgram", model: str = "aura-2-celeste-es"):
    """Create TTS provider based on configuration."""
    if provider == "local":
        logger.info("🔊 TTS Provider: Local (Mock)")
        from prospectiva.modulos.tts.local_tts import LocalTTS
        return LocalTTS()
    else:
        logger.info(f"🔊 TTS Provider: Deepgram (Aura-2, model={model})")
        from prospectiva.modulos.tts.deepgram_tts import DeepgramTTS
        return DeepgramTTS(api_key=deepgram_key, model=model)

# ---------------------------------------------------------------------------
# Worker functions
# ---------------------------------------------------------------------------

def _setup_logging():
    """Setup logging in worker processes."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S"
    )


def audio_worker(bus, my_queue, vosk_model_path, wake_word_engine,
                 porcupine_access_key, porcupine_keyword_path):
    """Audio process: microphone → wake word → VAD → SPEECH_COMPLETED."""
    _setup_logging()
    bus.set_private_queue(my_queue)
    from prospectiva.modulos.muta.audio_modules import SoundDeviceAudio, SileroVAD, PorcupineWakeWord
    from prospectiva.modulos.muta.vosk_wakeword import VoskWakeWord
    from prospectiva.procesos.audio import AudioProcess

    logger.info(f"[AudioWorker] Starting audio pipeline (wake_word={wake_word_engine})...")
    audio = SoundDeviceAudio(sample_rate=16000, channels=1, chunk_size=512)

    if wake_word_engine == "porcupine":
        if not porcupine_access_key:
            raise ValueError("PORCUPINE_ACCESS_KEY required for porcupine wake word engine")
        if porcupine_keyword_path:
            logger.info(f"[AudioWorker] Using custom Porcupine keyword: {porcupine_keyword_path}")
        else:
            logger.warning("[AudioWorker] No PORCUPINE_KEYWORD_PATH provided, using built-in 'porcupine'")
        wake_word = PorcupineWakeWord(
            access_key=porcupine_access_key,
            keyword_path=porcupine_keyword_path,
            sensitivity=0.7,
        )
    else:
        wake_word = VoskWakeWord(
            model_path=vosk_model_path,
            keyword="ronaldo",
            sample_rate=16000,
            cooldown_seconds=1.5,
            allow_partial=False,
        )
        wake_word.initialize()

    vad = SileroVAD(threshold=0.2)

    process = AudioProcess(bus, audio, wake_word, vad)
    process.run()


def orquestador_worker(bus, my_queue, system_prompt, groq_key, deepgram_key,
                       mcp_url, route_url, start_node, test_mode,
                       stt_provider, tts_provider, tts_model):
    """Orquestador with configurable providers."""
    _setup_logging()
    bus.set_private_queue(my_queue)
    from prospectiva.modulos.llm.groq_llm import GroqLLM
    from prospectiva.modulos.classifier.configurable_classifier import ConfigurableClassifier
    from prospectiva.procesos.orquestador import Orquestador

    # Create STT provider
    stt = get_stt_provider(groq_key, deepgram_key, stt_provider)

    # Create TTS provider
    tts = get_tts_provider(deepgram_key, tts_provider, model=tts_model)

    # LLM
    llm = GroqLLM(api_key=groq_key)
    
    # Classifier
    classifier = ConfigurableClassifier(config_path="config/commands.yaml")

    # MCP/Route clients
    if test_mode:
        from prospectiva.utils.mock_mcp_client import MockMCPClient
        from prospectiva.utils.mock_route_client import MockRouteClient
        mcp_client = MockMCPClient()
        route_client = MockRouteClient()
        logger.info("[OrquestadorWorker] Using MOCK clients (test mode)")
    else:
        from prospectiva.utils.mcp_client import MCPClient
        from prospectiva.utils.route_client import RouteClient
        mcp_token = os.getenv("MCP_BEARER_TOKEN", "")
        mcp_client = MCPClient(url=mcp_url, token=mcp_token) if mcp_url else None
        route_client = RouteClient(base_url=route_url) if route_url else None

    logger.info(f"[OrquestadorWorker] STT: {stt_provider}, TTS: {tts_provider}")
    
    if not tts.is_available():
        logger.warning("[OrquestadorWorker] ⚠️ TTS not available.")

    orquestador = Orquestador(
        bus, stt, llm, tts, classifier, system_prompt,
        mcp_client=mcp_client, route_client=route_client,
        start_node=start_node,
        use_native_tools=True
    )
    orquestador.run()


def playback_worker(bus, my_queue):
    """Audio playback: AUDIO_SYNTHESIZED → speaker."""
    _setup_logging()
    bus.set_private_queue(my_queue)
    from prospectiva.procesos.playback import AudioPlayback

    logger.info("[PlaybackWorker] Starting audio playback...")
    playback = AudioPlayback(bus)
    playback.run()


def movement_worker(bus, my_queue):
    """Movement execution: MOVEMENT_SEQUENCE_READY → execute."""
    _setup_logging()
    bus.set_private_queue(my_queue)
    from prospectiva.procesos.movement import MovementProcess

    logger.info("[MovementWorker] Starting movement executor...")
    movement = MovementProcess(bus)
    movement.run()


# ---------------------------------------------------------------------------
# Main Assistant
# ---------------------------------------------------------------------------

class Assistant:
    def __init__(self, test_mode: bool = False, text_mode: bool = False):
        self.event_bus = EventBus()
        self._running = True
        self._processes = []
        self.test_mode = test_mode
        self.text_mode = text_mode

    def start(self):
        logger.info("=" * 60)
        if self.test_mode:
            logger.info("🧪 MODO TEST - Usando datos mock")
        if self.text_mode:
            logger.info("📝 MODO TEXTO - Sin micrófono")
        logger.info("Asistente de Voz Universitario")
        logger.info("=" * 60)

        # Check API keys
        groq_key = os.getenv("GROQ_API_KEY")
        deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        if not groq_key:
            logger.error("❌ GROQ_API_KEY not found in .env")
            print("\n⚠️  ERROR: GROQ_API_KEY no encontrada.")
            return
        if not deepgram_key:
            logger.error("❌ DEEPGRAM_API_KEY not found in .env")
            print("\n⚠️  ERROR: DEEPGRAM_API_KEY no encontrada.")
            return

        # Resolve Vosk model path
        vosk_model_path = os.getenv("VOSK_MODEL_PATH", "./models/vosk/vosk-model-small-es-0.42")
        if vosk_model_path.startswith("./"):
            vosk_model_path = os.path.abspath(vosk_model_path)

        if not self.text_mode and not os.path.exists(vosk_model_path):
            logger.error(f"❌ Vosk model not found at: {vosk_model_path}")
            print("\n⚠️  ERROR: Modelo Vosk no encontrado.")
            return

        # Provider configuration
        stt_provider = os.getenv("STT_PROVIDER", "groq").lower()
        tts_provider = os.getenv("TTS_PROVIDER", "deepgram").lower()
        tts_model = os.getenv("TTS_MODEL", "aura-2-celeste-es")

        # Wake word engine configuration
        wake_word_engine = os.getenv("WAKE_WORD_ENGINE", "vosk").lower()
        porcupine_access_key = os.getenv("PORCUPINE_ACCESS_KEY", "")
        porcupine_keyword_path = os.getenv("PORCUPINE_KEYWORD_PATH", "")

        logger.info(
            f"⚙️  Config: STT={stt_provider}, TTS={tts_provider}, "
            f"TTS_MODEL={tts_model}, WAKE_WORD={wake_word_engine}"
        )
        
        # Config for new features
        mcp_url = os.getenv("MCP_URL", "") if not self.test_mode else ""
        route_url = os.getenv("ROUTE_API_URL", "") if not self.test_mode else ""
        start_node = os.getenv("ROBOT_START_NODE", "base")

        logger.info(f"📍 Robot start node: {start_node}")

        # Create per-process queues (must be done BEFORE spawning processes)
        audio_queue = mp.Queue()
        orq_queue = mp.Queue()
        playback_queue = mp.Queue()
        movement_queue = mp.Queue()
        text_queue = mp.Queue()
        all_queues = [audio_queue, orq_queue, playback_queue, movement_queue, text_queue]

        # Configure EventBus with all broadcast queues
        self.event_bus.set_broadcast_queues(all_queues)

        # Show available commands
        print("\n" + "=" * 60)
        print("  📋 COMANDOS DISPONIBLES")
        print("=" * 60)
        print("  Di 'ronaldo' seguido del comando:")
        print()
        print("  Navegación:")
        print("    • \"biomédica\"        → Edificio de Biomédica")
        print("    • \"giornale\"         → Edificio Giornale")
        print("    • \"biblioteca\"       → Biblioteca Central")
        print("    • \"cafetería\"        → Cafetería")
        print()
        print("  Robot:")
        print("    • \"siéntate\"         → Sentarse")
        print("    • \"baila\"            → Bailar")
        print("    • \"levántate\"        → Pararse")
        print("    • \"saluda\" / \"hola\" → Saludar")
        print("    • \"camina\"           → Caminar")
        print("    • \"detente\"          → Detenerse")
        print("=" * 60 + "\n")

        # Start processes
        self._processes = [
            mp.Process(target=orquestador_worker, args=(
                self.event_bus, orq_queue, SYSTEM_PROMPT, groq_key, deepgram_key,
                mcp_url, route_url, start_node, self.test_mode,
                stt_provider, tts_provider, tts_model
            ), name="Orquestador"),
            mp.Process(target=playback_worker, args=(self.event_bus, playback_queue), name="AudioPlayback"),
            mp.Process(target=movement_worker, args=(self.event_bus, movement_queue), name="MovementProcess"),
        ]

        if not self.text_mode:
            self._processes.append(
                mp.Process(target=audio_worker, args=(
                    self.event_bus, audio_queue, vosk_model_path,
                    wake_word_engine, porcupine_access_key, porcupine_keyword_path
                ), name="AudioProcess")
            )

        for p in self._processes:
            p.start()
            logger.info(f"Started process: {p.name} (PID={p.pid})")

        if self.text_mode:
            logger.info("✅ Asistente iniciado en modo texto. Escribe un comando.")
            logger.info("Escribe '/exit' para salir.")
            # Run text input directly in main process (stdin works reliably here)
            from prospectiva.procesos.text_input import TextInputProcess
            text_input = TextInputProcess(self.event_bus, text_queue)
            try:
                text_input.run()
            except KeyboardInterrupt:
                logger.info("\n⚠️ Interrupción recibida. Deteniendo...")
        else:
            logger.info("✅ Asistente iniciado. Dime 'ronaldo' para activar.")
            logger.info("Presiona Ctrl+C para detener.")

            # Wait for interrupt
            try:
                while self._running:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("\n⚠️ Interrupción recibida. Deteniendo...")

        self.stop()

    def stop(self):
        self._running = False
        logger.info("Deteniendo procesos...")
        for p in self._processes:
            if p.is_alive():
                p.terminate()
                p.join(timeout=2)
        logger.info("✅ Asistente detenido.")


if __name__ == "__main__":
    # Check flags
    test_mode = "--test" in sys.argv or "-t" in sys.argv
    text_mode = "--text" in sys.argv

    # Text mode uses fork to avoid stdin inheritance issues with spawn + pipes.
    # Audio mode keeps spawn for compatibility with torch/CUDA in child processes.
    if text_mode:
        mp.set_start_method("fork", force=True)
    else:
        mp.set_start_method("spawn", force=True)

    assistant = Assistant(test_mode=test_mode, text_mode=text_mode)
    assistant.start()
