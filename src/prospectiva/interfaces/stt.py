from abc import ABC, abstractmethod
from typing import Generator, Any, Dict, List

class SpeechToText(ABC):
    @abstractmethod
    def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        """Transcribe audio bytes to text."""
        ...

class TextGenerator(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str | None = None) -> Generator[str, None, None]:
        """Generate text fragments (streaming) from a prompt."""
        ...

    @abstractmethod
    def generate_with_tools(self, prompt: str, tools: List[Dict[str, Any]], 
                          system_prompt: str | None = None) -> Dict[str, Any]:
        """Generate text with tool calling support. Returns response with optional tool_calls."""
        ...

class TextToSpeech(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        """Synthesize text to audio bytes (e.g., WAV or MP3)."""
        ...

    def synthesize_stream(self, text: str):
        """Optional: yield audio chunks as they arrive. Default returns single chunk."""
        yield self.synthesize(text)

    @abstractmethod
    def is_available(self) -> bool:
        ...
