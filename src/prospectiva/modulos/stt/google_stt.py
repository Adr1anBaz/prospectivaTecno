import os
import time
import logging
from prospectiva.interfaces.stt import SpeechToText
from prospectiva.utils.audio_utils import preprocess_audio, get_audio_stats

logger = logging.getLogger(__name__)


class GoogleCloudSTT(SpeechToText):
    """
    Speech-to-Text usando Google Cloud Speech-to-Text API.

    Autentica via GOOGLE_APPLICATION_CREDENTIALS (Service Account JSON).
    Usa SpeechContext para boostear palabras del campus universitario.

    Usage:
        stt = GoogleCloudSTT()
        text = stt.transcribe(audio_bytes, sample_rate=16000)
    """

    def __init__(
        self,
        language: str = "es-MX",
        model: str = "latest_short",
    ):
        self.language = language
        self.model = model
        self.client = None
        logger.info(
            f"[GoogleCloudSTT] Initialized with lang={language}, model={model}"
        )

    def _ensure_client(self):
        if self.client is not None:
            return
        try:
            from google.cloud.speech_v1 import SpeechClient
            self.client = SpeechClient()
            logger.info("[GoogleCloudSTT] Authenticated via GOOGLE_APPLICATION_CREDENTIALS")
        except Exception as e:
            logger.error(f"[GoogleCloudSTT] Failed to create client: {e}")
            raise

    def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        if not audio_bytes or len(audio_bytes) < 3200:
            logger.warning("[GoogleCloudSTT] Audio too short, ignoring")
            return ""

        self._ensure_client()

        try:
            processed_bytes = preprocess_audio(
                audio_bytes,
                sample_rate=sample_rate,
                normalize=True,
                trim_silence_flag=True,
                target_db=-20.0,
            )
        except Exception as e:
            logger.warning(f"[GoogleCloudSTT] Preprocessing failed, using raw audio: {e}")
            processed_bytes = audio_bytes

        stats = get_audio_stats(processed_bytes, sample_rate)
        logger.info(
            f"[GoogleCloudSTT] Audio stats: duration={stats['duration']:.2f}s, "
            f"rms={stats['rms_db']:.1f}dB, peak={stats['peak']:.2f}"
        )

        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                return self._transcribe_impl(processed_bytes, sample_rate)
            except Exception as e:
                logger.error(
                    f"[GoogleCloudSTT] Error (attempt {attempt + 1}/{max_retries + 1}): {e}"
                )
                if attempt < max_retries:
                    time.sleep(1.0)
                else:
                    return ""

    def _transcribe_impl(self, audio_bytes: bytes, sample_rate: int) -> str:
        from google.cloud.speech_v1 import (
            RecognitionConfig,
            RecognitionAudio,
            SpeechContext,
        )

        # Speech context: boost words relevant to the university campus
        context = SpeechContext(
            phrases=[
                "biomédica",
                "bailar", "baila",
                "siéntate", "siénta",
                "levántate", "levanta",
                "saluda",
                "camina", "caminar",
                "detente", "detener",
                "giornale",
                "biblioteca",
                "cafetería",
                "pasillo a", "pasillo b", "pasillo c",
                "oficinas",
                "edificio",
                "llevame", "lleva",
                "navega",
                "quiero ir",
            ],
            boost=15,
        )

        config = RecognitionConfig(
            encoding=RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code=self.language,
            model=self.model,
            enable_automatic_punctuation=True,
            use_enhanced=True,
            profanity_filter=False,
            speech_contexts=[context],
        )

        audio = RecognitionAudio(content=audio_bytes)

        start = time.time()
        response = self.client.recognize(config=config, audio=audio)
        elapsed = time.time() - start

        text = ""
        for result in response.results:
            if result.alternatives:
                text += result.alternatives[0].transcript + " "

        text = text.strip()
        logger.info(f"[GoogleCloudSTT] Transcribed in {elapsed:.2f}s: '{text[:80]}...'")

        return text

    def is_available(self) -> bool:
        return True
