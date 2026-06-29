import os
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
    COOLDOWN:     Espera después de respuesta (evita feedback del TTS)
    
    Modo conversación: después de una respuesta conversacional, el Orquestador
    publica CONVERSATION_CONTINUING. El AudioProcess va a LISTENING en vez de
    WAKE_WORD, permitiendo hablar naturalmente sin wake word.
    
    Anti-feedback: mientras el TTS está reproduciéndose y unos segundos después,
    no se entra al modo conversación para evitar que el micrófono escuche la voz
    del asistente.
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
        self._conversation_pending = False  # conversation requested while TTS active
        
        # Speech collection
        self._speech_buffer = []
        self._silence_count = 0
        self._max_silence = 40  # ~1.3s of silence at 32ms/chunk
        
        # Prebuffer: guarda los últimos chunks mientras escucha wake word,
        # para no perder el inicio del comando hablado justo después de "ronaldo".
        self._prebuffer = []
        self._prebuffer_max_chunks = 16  # ~0.5s at 32ms/chunk
        
        # Listening timeout: if no speech captured within 15 seconds, abort
        self._listening_timeout = 470  # ~15 seconds at 32ms/chunk
        self._listening_count = 0
        
        # TTS playback muting: ignore microphone input while assistant is speaking
        self._tts_playing = False
        
        # Post-response cooldown: after sending SPEECH_COMPLETED, wait ~1 second
        self._cooldown_chunks = 31  # ~1 second
        self._cooldown_count = 0

        # TTS anti-feedback tracking
        self._tts_chunk_count = 0
        self._post_tts_cooldown_count = 0
        self._min_post_tts_cooldown_chunks = max(1, int(os.getenv("POST_TTS_COOLDOWN_MS", "3000")) // 32)
        self._max_post_tts_cooldown_chunks = 250  # ~8s max

        # VAD streak: require N consecutive VAD-positive chunks before capturing
        # in conversation mode, to avoid triggering on noise/echo spikes
        self._vad_streak = 0
        self._min_vad_streak = 3

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
        """Non-blocking check for conversation events and TTS state."""
        # Decrement post-TTS echo cooldown every chunk, regardless of state
        if self._post_tts_cooldown_count > 0:
            self._post_tts_cooldown_count -= 1
            if self._post_tts_cooldown_count == 0:
                logger.info("[AudioProcess] Post-TTS echo cooldown ended")

        # Process pending conversation request once TTS + echo cooldown finished
        if (self._conversation_pending and not self._tts_playing
                and self._post_tts_cooldown_count <= 0
                and self._state in ("WAKE_WORD", "COOLDOWN")):
            self._enter_listening_mode("CONVERSATION_PENDING")

        while True:
            event = self.event_bus.get(timeout=0.001)
            if event is None:
                break
            event_type, payload = event
            if event_type == "CONVERSATION_CONTINUING":
                if self._tts_playing or self._post_tts_cooldown_count > 0:
                    # Defer entering conversation mode until assistant stops talking
                    self._conversation_pending = True
                    logger.info("[AudioProcess] Conversation requested but TTS active, deferring...")
                elif self._state in ("WAKE_WORD", "COOLDOWN"):
                    self._enter_listening_mode("CONVERSATION_CONTINUING")
                else:
                    self._conversation_mode = True
                    self._conversation_silence = 0
            elif event_type == "CONVERSATION_END":
                self._conversation_mode = False
                self._conversation_pending = False
                if self._state == "LISTENING":
                    self._abort_listening()
            elif event_type in ("AUDIO_STREAM_START", "AUDIO_SYNTHESIZED"):
                self._tts_playing = True
                self._tts_chunk_count = 0
                self._post_tts_cooldown_count = 0
                # Flush any audio captured just before TTS started (echo edge case)
                self._speech_buffer = []
                self._silence_count = 0
                logger.debug("[AudioProcess] TTS playback started — speech buffer flushed")
            elif event_type == "AUDIO_STREAM_CHUNK":
                self._tts_chunk_count += 1
            elif event_type == "AUDIO_STREAM_END":
                self._tts_playing = False
                # Adaptive cooldown: duration TTS * 1.5, min 3s, max 8s
                adaptive = max(self._min_post_tts_cooldown_chunks,
                               int(self._tts_chunk_count * 1.5))
                self._post_tts_cooldown_count = min(adaptive, self._max_post_tts_cooldown_chunks)
                self._tts_chunk_count = 0
                logger.info(f"[AudioProcess] TTS playback ended, post-TTS cooldown {self._post_tts_cooldown_count * 32}ms")

    def _enter_listening_mode(self, reason: str):
        """Transition to listening mode."""
        # Skip if assistant is still speaking or echo hasn't decayed
        if self._tts_playing or self._post_tts_cooldown_count > 0:
            self._conversation_pending = True
            logger.info(f"[AudioProcess] Deferred {reason}: TTS active or echo cooldown")
            return

        self._conversation_mode = True
        self._conversation_pending = False
        self._state = "LISTENING"
        self._speech_buffer = []
        self._silence_count = 0
        self._listening_count = 0
        self._conversation_silence = 0
        self._vad_streak = 0
        self.vad.reset()
        logger.info(f"[AudioProcess] 🗣️ Conversation mode ({reason}) — listening for reply...")

    def _detect_wake_word(self, chunk: np.ndarray):
        # Mantener prebuffer circular mientras escuchamos wake word
        self._prebuffer.append(chunk)
        if len(self._prebuffer) > self._prebuffer_max_chunks:
            self._prebuffer.pop(0)
        
        if len(chunk) != self.wake_word.frame_length:
            return
        if self.wake_word.process(chunk):
            logger.info("[AudioProcess] ✅ Wake word detected! Listening for command...")
            self.event_bus.publish("WAKE_WORD_DETECTED", {"timestamp": time.time()})
            self._conversation_mode = False
            self._state = "LISTENING"
            # Sembrar el buffer con el prebuffer para no perder el inicio del comando
            self._speech_buffer = self._prebuffer.copy()
            self._prebuffer = []
            self._silence_count = 0
            self._listening_count = 0
            self._conversation_silence = 0
            self._vad_streak = 0
            self.vad.reset()

    def _collect_speech(self, chunk: np.ndarray):
        self._listening_count += 1
        
        # Timeout: if no speech captured within 15 seconds, abort
        if self._listening_count > self._listening_timeout:
            logger.info("[AudioProcess] ⏱ Listening timeout (15s), no command detected")
            self._abort_listening()
            return
        
        # Ignore audio while assistant is speaking (prevents TTS echo loops)
        if self._tts_playing:
            return
        
        # Conversation silence timeout: if no speech for ~15s, end conversation
        if self._conversation_mode:
            self._conversation_silence += 1
            if self._conversation_silence > self._conversation_timeout:
                logger.info("[AudioProcess] ⏱ Conversation silence timeout (15s), ending conversation")
                self._conversation_mode = False
                self._abort_listening()
                return
        
        # VAD detection
        is_speech = self.vad.is_speech(chunk)

        if is_speech:
            # In conversation mode, require N consecutive VAD-positive chunks
            # before starting capture to avoid triggering on noise/echo spikes
            if self._conversation_mode and len(self._speech_buffer) == 0:
                self._vad_streak += 1
                if self._vad_streak < self._min_vad_streak:
                    return
                self._vad_streak = 0

            self._speech_buffer.append(chunk)
            self._silence_count = 0
            self._conversation_silence = 0
        else:
            self._vad_streak = 0
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
        # Count down normal post-response cooldown
        if self._cooldown_count > 0:
            self._cooldown_count -= 1

        # Only transition when normal cooldown finishes
        if self._cooldown_count <= 0:
            # If conversation was deferred because TTS was active, enter it now
            # but only after post-TTS echo cooldown also finished
            if self._conversation_pending and self._post_tts_cooldown_count <= 0:
                self._enter_listening_mode("CONVERSATION_PENDING")
            elif self._conversation_mode:
                self._state = "LISTENING"
                self._speech_buffer = []
                self._silence_count = 0
                self._listening_count = 0
                self._conversation_silence = 0
                self._vad_streak = 0
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
        self._vad_streak = 0
        self.wake_word.reset()
        logger.info("[AudioProcess] Back to wake word listening")

    def stop(self):
        self._running = False
