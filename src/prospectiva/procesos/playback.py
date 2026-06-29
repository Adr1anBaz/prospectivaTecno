import numpy as np
import sounddevice as sd
import time
import logging
import wave
from io import BytesIO
from prospectiva.bus.event_bus import EventBus

logger = logging.getLogger(__name__)

class AudioPlayback:
    """Audio playback handler with streaming support."""

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
            elif event_type == "AUDIO_STREAM_START":
                self._start_stream(payload)
            elif event_type == "AUDIO_STREAM_CHUNK":
                self._feed_stream(payload)
            elif event_type == "AUDIO_STREAM_END":
                self._end_stream()
        logger.info("[AudioPlayback] Stopped")

    # ── legacy full-audio playback ──

    def _play_audio(self, payload: dict):
        audio_bytes = payload.get("audio")
        if not audio_bytes:
            return
        try:
            w = wave.open(BytesIO(audio_bytes), "rb")
            frames = w.readframes(w.getnframes())
            audio_np = np.frombuffer(frames, dtype=np.int16)
            sr = w.getframerate()
            w.close()
            sd.play(audio_np, sr)
            sd.wait()
            logger.info(f"[AudioPlayback] Played {len(audio_np)} samples at {sr}Hz")
        except Exception as e:
            logger.error(f"[AudioPlayback] Error: {e}")

    # ── streaming playback ──

    def _start_stream(self, payload: dict):
        try:
            header = payload.get("header", b"")
            w = wave.open(BytesIO(header), "rb")
            self._stream_sr = w.getframerate()
            self._stream_channels = w.getnchannels()
            self._stream_width = w.getsampwidth()
            w.close()
            self._stream_out = sd.OutputStream(
                samplerate=self._stream_sr,
                channels=self._stream_channels,
                dtype="int16",
                blocksize=1024,
            )
            self._stream_out.start()
        except Exception as e:
            logger.error(f"[AudioPlayback] Stream start error: {e}")
            self._stream_out = None

    def _feed_stream(self, payload: dict):
        chunk = payload.get("chunk", b"")
        if not chunk or not hasattr(self, "_stream_out") or self._stream_out is None:
            return
        try:
            data = np.frombuffer(chunk, dtype=np.int16).reshape(-1, self._stream_channels)
            self._stream_out.write(data)
        except Exception as e:
            logger.error(f"[AudioPlayback] Feed error: {e}")

    def _end_stream(self):
        if hasattr(self, "_stream_out") and self._stream_out is not None:
            self._stream_out.stop()
            self._stream_out.close()
            self._stream_out = None

    def stop(self):
        self._end_stream()
        self._running = False
