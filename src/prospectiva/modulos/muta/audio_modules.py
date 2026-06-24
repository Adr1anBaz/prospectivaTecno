import numpy as np
import sounddevice as sd
import logging
from prospectiva.interfaces.audio import AudioInput, WakeWordDetector, VoiceActivityDetector

logger = logging.getLogger(__name__)

class SoundDeviceAudio(AudioInput):
    """Audio input using sounddevice (PortAudio)."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 512):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.dtype = np.int16
        self._stream = None
        self._buffer = []

    def start_stream(self) -> None:
        logger.info(f"[Audio] Starting stream: {self.sample_rate}Hz, {self.channels}ch, chunk={self.chunk_size}")
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            blocksize=self.chunk_size,
        )
        self._stream.start()

    def stop_stream(self) -> None:
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
            logger.info("[Audio] Stream stopped")

    def read_chunk(self) -> np.ndarray:
        if self._stream is None:
            raise RuntimeError("Stream not started")
        data, overflowed = self._stream.read(self.chunk_size)
        if overflowed:
            logger.warning("[Audio] Input overflow")
        return data.flatten()

class PorcupineWakeWord(WakeWordDetector):
    """Wake word detection using Porcupine (Picovoice)."""

    def __init__(self, access_key: str | None = None, keyword_path: str | None = None, sensitivity: float = 0.5):
        import pvporcupine
        if keyword_path and not access_key:
            raise ValueError("access_key required when using custom keyword_path")
        if keyword_path:
            self._handle = pvporcupine.create(
                access_key=access_key,
                keyword_paths=[keyword_path],
                sensitivities=[sensitivity]
            )
        else:
            self._handle = pvporcupine.create(access_key=access_key, keywords=["porcupine"])
        self.frame_length = self._handle.frame_length
        self.sample_rate = self._handle.sample_rate
        logger.info(f"[Porcupine] Initialized: frame_length={self.frame_length}, sr={self.sample_rate}")

    def process(self, audio_chunk: np.ndarray) -> bool:
        """Process audio chunk. Returns True if wake word detected."""
        if len(audio_chunk) != self.frame_length:
            return False
        result = self._handle.process(audio_chunk.tolist())
        return result >= 0

    def reset(self) -> None:
        pass

    def __del__(self):
        if hasattr(self, "_handle") and self._handle:
            self._handle.delete()

class SileroVAD(VoiceActivityDetector):
    """Voice Activity Detection using Silero VAD."""

    def __init__(self, threshold: float = 0.3):
        from silero_vad import load_silero_vad, read_audio
        self.model = load_silero_vad()
        self.threshold = threshold
        logger.info(f"[SileroVAD] Initialized with threshold={threshold}")

    def is_speech(self, audio_chunk: np.ndarray) -> bool:
        """Returns True if speech detected."""
        import torch
        audio_float = audio_chunk.astype(np.float32) / 32768.0
        audio_tensor = torch.from_numpy(audio_float)
        if audio_tensor.dim() == 1:
            audio_tensor = audio_tensor.unsqueeze(0)
        with torch.no_grad():
            speech_prob = self.model(audio_tensor, 16000).item()
        is_speech = speech_prob > self.threshold
        # Debug: log VAD probability when speech is detected
        if is_speech:
            logger.debug(f"[SileroVAD] Speech detected (prob={speech_prob:.3f})")
        return is_speech

    def reset(self) -> None:
        pass
