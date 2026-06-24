import numpy as np
import sounddevice as sd
import time
import logging
from io import BytesIO
from prospectiva.bus.event_bus import EventBus

logger = logging.getLogger(__name__)

class AudioPlayback:
    """Audio playback handler."""

    def __init__(self, event_bus: EventBus, sample_rate: int = 16000):
        self.event_bus = event_bus
        self.sample_rate = sample_rate
        self._running = True

    def run(self):
        logger.info("[AudioPlayback] Started")
        while self._running:
            event = self.event_bus.get(timeout=1.0)
            if event is None:
                continue
            event_type, payload = event
            if event_type == "AUDIO_SYNTHESIZED":
                self._play_audio(payload)
        logger.info("[AudioPlayback] Stopped")

    def _play_audio(self, payload: dict):
        audio_bytes = payload.get("audio")
        if not audio_bytes:
            return
        try:
            # Try to play as WAV
            try:
                import wave
                wav = wave.open(BytesIO(audio_bytes), "rb")
                frames = wav.readframes(wav.getnframes())
                audio_np = np.frombuffer(frames, dtype=np.int16)
                sr = wav.getframerate()
                wav.close()
            except Exception:
                # Fallback: assume raw PCM
                audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
                sr = self.sample_rate
            sd.play(audio_np, sr)
            sd.wait()
            logger.info(f"[AudioPlayback] Played {len(audio_np)} samples at {sr}Hz")
        except Exception as e:
            logger.error(f"[AudioPlayback] Error playing audio: {e}")

    def stop(self):
        self._running = False
