import os
import time
import logging
import io
from prospectiva.interfaces.stt import TextToSpeech

logger = logging.getLogger(__name__)

class DeepgramTTS(TextToSpeech):
    """Deepgram Text-to-Speech using the Aura-2 model."""

    def __init__(self, api_key: str | None = None, model: str = "aura-2-celeste-es"):
        try:
            from deepgram import DeepgramClient
            key = api_key or os.getenv("DEEPGRAM_API_KEY")
            self.client = DeepgramClient(api_key=key)
            self.model = model
            self.available = True
            logger.info(f"[DeepgramTTS] Initialized with model={model}")
        except Exception as e:
            logger.error(f"[DeepgramTTS] Error initializing: {e}")
            self.available = False

    def synthesize(self, text: str) -> bytes:
        if not self.available:
            logger.warning("[DeepgramTTS] Not available, skipping synthesis")
            return b""
        try:
            logger.info(f"[DeepgramTTS] Synthesizing: '{text[:50]}...'")
            
            # Deepgram SDK v7: generate returns Iterator[bytes]
            response = self.client.speak.v1.audio.generate(
                text=text,
                model=self.model,
                encoding="linear16",
                container="wav",
            )
            
            # Collect all bytes from the iterator
            audio_bytes = b"".join(response)
            
            logger.info(f"[DeepgramTTS] Synthesized {len(audio_bytes)} bytes")
            return audio_bytes
        except Exception as e:
            logger.error(f"[DeepgramTTS] Error: {e}")
            return b""

    def is_available(self) -> bool:
        return self.available
