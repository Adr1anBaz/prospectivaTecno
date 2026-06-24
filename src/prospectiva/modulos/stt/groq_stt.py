import os
import time
import logging
from prospectiva.interfaces.stt import SpeechToText
from prospectiva.utils.audio_utils import preprocess_audio, pcm_to_wav_bytes, get_audio_stats

logger = logging.getLogger(__name__)

class GroqSTT(SpeechToText):
    def __init__(self, api_key: str | None = None, model: str = "whisper-large-v3-turbo"):
        from groq import Groq
        self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
        self.model = model
        logger.info(f"[GroqSTT] Initialized with model={model}")

    def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        if not audio_bytes or len(audio_bytes) < 3200:  # ~0.1s minimum
            logger.warning("[GroqSTT] Audio too short, ignoring")
            return ""

        # Preprocess audio: trim silence + normalize
        try:
            processed_bytes = preprocess_audio(
                audio_bytes,
                sample_rate=sample_rate,
                normalize=True,
                trim_silence_flag=True,
                target_db=-20.0,
            )
        except Exception as e:
            logger.warning(f"[GroqSTT] Preprocessing failed, using raw audio: {e}")
            processed_bytes = audio_bytes

        # Log audio stats
        stats = get_audio_stats(processed_bytes, sample_rate)
        logger.info(
            f"[GroqSTT] Audio stats: duration={stats['duration']:.2f}s, "
            f"rms={stats['rms_db']:.1f}dB, peak={stats['peak']:.2f}"
        )

        # Build WAV
        wav_bytes = pcm_to_wav_bytes(processed_bytes, sample_rate=sample_rate, channels=1)

        # Retry logic
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                start = time.time()
                transcription = self.client.audio.transcriptions.create(
                    file=("audio.wav", wav_bytes),
                    model=self.model,
                    language="es",
                    response_format="text",
                    timeout=30.0
                )
                elapsed = time.time() - start
                text = transcription.text if hasattr(transcription, "text") else str(transcription)
                logger.info(f"[GroqSTT] Transcribed in {elapsed:.2f}s: '{text[:80]}...'")
                return text
            except Exception as e:
                logger.error(f"[GroqSTT] Error (attempt {attempt + 1}/{max_retries + 1}): {e}")
                if attempt < max_retries:
                    time.sleep(1.0)
                else:
                    return ""
