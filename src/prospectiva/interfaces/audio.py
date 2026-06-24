from abc import ABC, abstractmethod
import numpy as np

class AudioInput(ABC):
    @abstractmethod
    def start_stream(self) -> None:
        ...

    @abstractmethod
    def stop_stream(self) -> None:
        ...

    @abstractmethod
    def read_chunk(self) -> np.ndarray:
        ...

class WakeWordDetector(ABC):
    @abstractmethod
    def process(self, audio_chunk: np.ndarray) -> bool:
        """Return True if wake word detected."""
        ...

    @abstractmethod
    def reset(self) -> None:
        ...

class VoiceActivityDetector(ABC):
    @abstractmethod
    def is_speech(self, audio_chunk: np.ndarray) -> bool:
        """Return True if speech detected in chunk."""
        ...

    @abstractmethod
    def reset(self) -> None:
        ...
