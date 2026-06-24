import time
import logging
import sys
from prospectiva.bus.event_bus import EventBus

logger = logging.getLogger(__name__)


class TextInputProcess:
    """
    Process that reads text from stdin instead of microphone audio.

    Simulates the full audio pipeline:
    - Normal mode: requires 'ronaldo <comando>' prefix
    - Conversation mode: any input is treated as a reply

    Special commands:
      /wake  -> simulate wake word detection
      /end   -> end conversation mode
      /exit  -> stop the assistant
      exit   -> stop the assistant
    """

    def __init__(self, event_bus: EventBus, my_queue):
        self.event_bus = event_bus
        self.event_bus.set_private_queue(my_queue)
        self._running = True
        self._conversation_mode = False
        self._wake_word = "ronaldo"

    def run(self):
        logger.info("[TextInputProcess] Started")
        print("\n" + "=" * 60)
        print("  📝 MODO TEXTO ACTIVADO")
        print("=" * 60)
        print("  Escribe comandos como si los dijeras:")
        print(f"    • '{self._wake_word} llévame a biomédica' → comando con wake word")
        print("    • (en conversación) 'gracias' → respuesta directa")
        print("")
        print("  Comandos especiales:")
        print("    • /wake  → simular detección de wake word")
        print("    • /end   → terminar modo conversación")
        print("    • /exit  → salir")
        print("=" * 60 + "\n")

        while self._running:
            self._drain_events()
            prompt = self._get_prompt()
            try:
                line = input(prompt)
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            self._handle_input(line.strip())

        logger.info("[TextInputProcess] Stopped")

    def _drain_events(self):
        """Check for CONVERSATION_CONTINUING / CONVERSATION_END events."""
        while True:
            event = self.event_bus.get(timeout=0.001)
            if event is None:
                break
            event_type, _ = event
            if event_type == "CONVERSATION_CONTINUING":
                if not self._conversation_mode:
                    self._conversation_mode = True
                    print("\n🗣️ Entrando a modo conversación...")
            elif event_type == "CONVERSATION_END":
                if self._conversation_mode:
                    self._conversation_mode = False
                    print("\n🔇 Modo conversación terminado.")

    def _get_prompt(self) -> str:
        if self._conversation_mode:
            return "🗣️  > "
        return f"🎤 [{self._wake_word}] > "

    def _handle_input(self, line: str):
        if not line:
            return

        lower = line.lower()

        # Exit commands
        if lower in ("/exit", "/quit", "exit", "quit"):
            print("👋 Saliendo...")
            self._running = False
            self.event_bus.publish("STOP", {"reason": "user_exit"})
            time.sleep(0.2)  # Give main process time to receive STOP
            return

        # End conversation
        if lower == "/end":
            self._conversation_mode = False
            self.event_bus.publish("CONVERSATION_END", {})
            print("🔇 Modo conversación terminado.")
            return

        # Simulate wake word
        if lower == "/wake":
            self.event_bus.publish("WAKE_WORD_DETECTED", {"timestamp": time.time()})
            print("👂 Wake word simulado. Ahora escribe el comando.")
            return

        # Conversation mode: direct input
        if self._conversation_mode:
            self.event_bus.publish("TEXT_INPUT", {"text": line})
            return

        # Normal mode: require wake word prefix
        prefix = f"{self._wake_word} "
        prefix_short = f"{self._wake_word[0]} "
        if lower.startswith(prefix) or lower.startswith(prefix_short):
            text = line[len(prefix):].strip() if lower.startswith(prefix) else line[len(prefix_short):].strip()
            if text:
                # Simulate wake word detection first, then the command
                self.event_bus.publish("WAKE_WORD_DETECTED", {"timestamp": time.time()})
                time.sleep(0.05)
                self.event_bus.publish("TEXT_INPUT", {"text": text})
        else:
            print(f"ℹ️  Di '{self._wake_word} <comando>' o usa /wake para activar.")
