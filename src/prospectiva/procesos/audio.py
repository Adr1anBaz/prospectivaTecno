import numpy as np
import time
import logging
import multiprocessing as mp
from prospectiva.bus.event_bus import EventBus
from prospectiva.interfaces.audio import AudioInput, WakeWordDetector, VoiceActivityDetector

logger = logging.getLogger(__name__)

class AudioProcess:
    """
    Process that handles microphone, wake word, and VAD.
    
    State machine:
    WAKE_WORD → LISTENING → COOLDOWN → WAKE_WORD (or LISTENING if in conversation mode)
    
    WAKE_WORD:    Escucha "ronaldo" con VoskWakeWord
    LISTENING:    Captura audio del comando con VAD
    COOLDOWN:     Espera ~1s después de respuesta (evita feedback del TTS)
    
    Modo conversación: después de una respuesta conversacional, el Orquestador
    publica CONVERSATION_CONTINUING. El AudioProcess va a LISTENING en vez de
    WAKE_WORD, permitiendo hablar naturalmente sin wake word.
    """

    def __init__(self, event_bus: EventBus, audio_input: AudioInput,
                 wake_word: WakeWordDetector, vad: VoiceActivityDetector):
        self.event_bus = event_bus
        self.audio = audio_input
        self.wake_word = wake_word
        self.vad = vad
        self._running = True
        
        # State machine
        self._state = "WAKE_WORD"  # WAKE_WORD | LISTENING | COOLDOWN
        
        # Conversation mode: if True, after cooldown go to LISTENING
        self._conversation_mode = False
        self._conversation_timeout = 470  # ~15 seconds of silence in conversation mode
        self._conversation_silence = 0
        
        # Speech collection
        self._speech_buffer = []
        self._silence_count = 0
        self._max_silence = 40  # ~1.3s of silence at 32ms/chunk
        
        # Listening timeout: if no speech captured within 8 seconds, abort
        self._listening_timeout = 250  # ~8 seconds
        self._listening_count = 0
        
        # Post-response cooldown: after sending SPEECH_COMPLETED, wait ~1 second
        self._cooldown_chunks = 31  # ~1 second
        self._cooldown_count = 0

    def run(self):
        logger.info("[AudioProcess] Started")
        self.audio.start_stream()
        try:
            while self._running:
                chunk = self.audio.read_chunk()
                
                # Check for conversation events BEFORE state processing
                self._check_conversation_events()
                
                if self._state == "WAKE_WORD":
                    self._detect_wake_word(chunk)
                    
                elif self._state == "LISTENING":
                    self._collect_speech(chunk)
                    
                elif self._state == "COOLDOWN":
                    self._handle_cooldown(chunk)
                        
        except Exception as e:
            logger.error(f"[AudioProcess] Error: {e}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            self.audio.stop_stream()
        logger.info("[AudioProcess] Stopped")

    def _check_conversation_events(self):
        """Non-blocking check for CONVERSATION_CONTINUING / CONVERSATION_END events."""
        while True:
            event = self.event_bus.get(timeout=0.001)
            if event is None:
                break
            event_type, payload = event
            if event_type == "CONVERSATION_CONTINUING":
                if self._state in ("WAKE_WORD", "COOLDOWN"):
                    self._enter_listening_mode("CONVERSATION_CONTINUING")
                else:
                    self._conversation_mode = True
                    self._conversation_silence = 0
            elif event_type == "CONVERSATION_END":
                self._conversation_mode = False
                if self._state == "LISTENING":
                    self._abort_listening()

    def _enter_listening_mode(self, reason: str):
        """Transition to listening mode."""
        self._conversation_mode = True
        self._state = "LISTENING"
        self._speech_buffer = []
        self._silence_count = 0
        self._listening_count = 0
        self._conversation_silence = 0
        self.vad.reset()
        logger.info(f"[AudioProcess] 🗣️ Conversation mode ({reason}) — listening for reply...")

    def _detect_wake_word(self, chunk: np.ndarray):
        if len(chunk) != self.wake_word.frame_length:
            return
        if self.wake_word.process(chunk):
            logger.info("[AudioProcess] ✅ Wake word detected! Listening for command...")
            self.event_bus.publish("WAKE_WORD_DETECTED", {"timestamp": time.time()})
            self._conversation_mode = False
            self._state = "LISTENING"
            self._speech_buffer = []
            self._silence_count = 0
            self._listening_count = 0
            self._conversation_silence = 0
            self.vad.reset()

    def _collect_speech(self, chunk: np.ndarray):
        self._listening_count += 1
        
        # Timeout: if no speech captured within 8 seconds, abort
        if self._listening_count > self._listening_timeout:
            logger.info("[AudioProcess] ⏱ Listening timeout (8s), no command detected")
            self._abort_listening()
            return
        
        # VAD detection: immediately start collecting audio
        is_speech = self.vad.is_speech(chunk)
        if is_speech:
            self._speech_buffer.append(chunk)
            self._silence_count = 0
        else:
            self._silence_count += 1
            if self._silence_count >= self._max_silence:
                self._finish_speech()
            else:
                # Still append non-speech chunks to avoid cutting off the end
                self._speech_buffer.append(chunk)

    def _finish_speech(self):
        # Minimum speech: ~0.3 second = 10 chunks
        min_chunks = 10
        if len(self._speech_buffer) < min_chunks:
            logger.info(f"[AudioProcess] Speech too short ({len(self._speech_buffer)} chunks), ignoring")
            self._abort_listening()
            return
            
        audio = np.concatenate(self._speech_buffer)
        # IMPORTANT: audio is already int16 from sounddevice, do NOT multiply by 32767
        # that would cause overflow and corrupt the audio.
        audio_bytes = audio.astype(np.int16).tobytes()
        self.event_bus.publish("SPEECH_COMPLETED", {
            "audio": audio_bytes,
            "sample_rate": self.audio.sample_rate
        })
        duration = len(audio) / self.audio.sample_rate
        logger.info(f"[AudioProcess] ✅ Speech captured: {len(audio)} samples ({duration:.1f}s)")
        
        # Enter cooldown to prevent feedback loops
        self._state = "COOLDOWN"
        self._cooldown_count = self._cooldown_chunks
        self._speech_buffer = []
        self._silence_count = 0

    def _handle_cooldown(self, chunk: np.ndarray):
        """Handle cooldown state."""
        self._cooldown_count -= 1
        if self._cooldown_count <= 0:
            if self._conversation_mode:
                self._state = "LISTENING"
                self._speech_buffer = []
                self._silence_count = 0
                self._listening_count = 0
                self._conversation_silence = 0
                self.vad.reset()
                logger.info("[AudioProcess] 🗣️ Conversation mode — listening for reply...")
            else:
                self._state = "WAKE_WORD"
                self.wake_word.reset()
                logger.info("[AudioProcess] Cooldown ended, listening for wake word")

    def _abort_listening(self):
        """Abort listening and return to wake word detection."""
        self._conversation_mode = False
        self._state = "WAKE_WORD"
        self._speech_buffer = []
        self._silence_count = 0
        self._listening_count = 0
        self._conversation_silence = 0
        self.wake_word.reset()
        logger.info("[AudioProcess] Back to wake word listening")

    def stop(self):
        self._running = False
