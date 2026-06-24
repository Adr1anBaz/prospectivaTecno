import os
import time
import logging
from typing import Optional
from prospectiva.interfaces.stt import TextToSpeech

logger = logging.getLogger(__name__)

class LocalTTS(TextToSpeech):
    """
    Placeholder for local/offline TTS.
    
    This is a mock implementation that prints text to console
    instead of generating audio. In production, integrate with:
    - Piper TTS (fast, lightweight, runs on Raspberry Pi)
    - Coqui TTS
    - Mozilla TTS
    - Or any other local TTS engine
    
    Usage:
        tts = LocalTTS()
        audio_bytes = tts.synthesize("Hola mundo")
        # In mock mode: returns empty bytes and prints to console
    """

    def __init__(self, model_path: str | None = None):
        self.model_path = model_path or os.getenv("LOCAL_TTS_MODEL", "")
        self.available = True
        logger.info("[LocalTTS] Initialized (MOCK - no audio generation)")
        logger.info("[LocalTTS] ⚠️ To enable real local TTS, integrate with Piper TTS or similar")

    def synthesize(self, text: str) -> bytes:
        """
        Synthesize text to speech.
        
        Currently returns empty bytes (mock).
        Prints the text to console for debugging.
        """
        logger.info(f"[LocalTTS] 🎙️ (MOCK) Would speak: '{text}'")
        print(f"\n🎙️ [LocalTTS] Speaking: '{text}'")
        
        # In a real implementation, this would:
        # 1. Load the TTS model
        # 2. Generate audio waveform
        # 3. Return audio bytes
        
        # For now, return empty bytes
        # This prevents audio playback but allows the system to continue
        return b""

    def is_available(self) -> bool:
        return self.available
