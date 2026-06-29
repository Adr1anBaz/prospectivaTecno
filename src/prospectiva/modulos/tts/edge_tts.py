import os
import io
import logging
from pydub import AudioSegment
from prospectiva.interfaces.stt import TextToSpeech

logger = logging.getLogger(__name__)


class EdgeTTS(TextToSpeech):
    """Microsoft Edge TTS via edge-tts. Rapido, gratuito, streaming real."""

    def __init__(self, voice: str = "es-MX-JorgeNeural"):
        self.voice = voice
        self.available = True
        logger.info(f"[EdgeTTS] voice={voice}")

    def _mp3_to_wav(self, mp3_data: bytes) -> bytes:
        seg = AudioSegment.from_mp3(io.BytesIO(mp3_data))
        buf = io.BytesIO()
        seg.export(buf, format="wav")
        return buf.getvalue()

    def synthesize(self, text: str) -> bytes:
        try:
            import edge_tts
            import asyncio
            communicate = edge_tts.Communicate(text, self.voice)
            mp3 = b""
            for chunk in asyncio.run(communicate.stream()):
                if chunk["type"] == "audio":
                    mp3 += chunk["data"]
            return self._mp3_to_wav(mp3) if mp3 else b""
        except Exception as e:
            logger.error(f"[EdgeTTS] Error: {e}")
            return b""

    def synthesize_stream(self, text: str):
        try:
            import edge_tts
            import asyncio

            async def _collect():
                communicate = edge_tts.Communicate(text, self.voice)
                chunks = []
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        chunks.append(chunk["data"])
                return chunks

            mp3_chunks = asyncio.run(_collect())
            if not mp3_chunks:
                return

            # edge-tts genera MP3 en tiempo real. Convertimos cada chunk
            # combinado a WAV y partimos para streaming.
            full_mp3 = b"".join(mp3_chunks)
            wav = self._mp3_to_wav(full_mp3)

            # Partir el WAV en chunks (~16KB cada uno) para streaming
            CHUNK_SIZE = 16384
            for i in range(0, len(wav), CHUNK_SIZE):
                yield wav[i:i + CHUNK_SIZE]
        except Exception as e:
            logger.error(f"[EdgeTTS] Stream error: {e}")

    def is_available(self) -> bool:
        return self.available
