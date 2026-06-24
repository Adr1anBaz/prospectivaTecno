import os
import json
import time
import logging
import numpy as np
from prospectiva.interfaces.audio import WakeWordDetector

logger = logging.getLogger(__name__)


class VoskWakeWord(WakeWordDetector):
    """
    Wake word detector using Vosk offline speech recognition.
    
    NO usamos SetGrammar porque fuerza a Vosk a mapear cualquier sonido a
    las palabras del grammar, causando falsos positivos (e.g. "oye" → "oye blu").
    En su lugar usamos el modelo completo y verificamos partial/final results.
    """

    def __init__(
        self,
        model_path: str,
        keyword: str = "ronaldo",
        sample_rate: int = 16000,
        cooldown_seconds: float = 1.5,
        allow_partial: bool = False,
    ):
        self.model_path = model_path
        self.keyword = keyword.lower().strip()
        self.sample_rate = sample_rate
        self.cooldown_seconds = cooldown_seconds
        self.allow_partial = allow_partial
        self.model = None
        self.rec = None
        self._initialized = False
        self._last_partial = ""
        self._last_final = ""
        self._last_detection_time = 0
        # Frame length expected by AudioProcess (512 samples = 32ms @ 16kHz)
        self.frame_length = 512

    def initialize(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Vosk model not found at: {self.model_path}\n"
                f"Download it with: python scripts/download_vosk_model.py"
            )

        try:
            from vosk import Model, KaldiRecognizer
        except ImportError as e:
            raise ImportError("Vosk not installed. Run: uv add vosk") from e

        logger.info(f"[VoskWakeWord] Loading model from: {self.model_path}")
        self.model = Model(self.model_path)
        self.rec = KaldiRecognizer(self.model, self.sample_rate)
        self._initialized = True
        self._last_partial = ""
        self._last_final = ""
        self._last_detection_time = 0
        logger.info(f"[VoskWakeWord] Initialized, listening for: '{self.keyword}' (partial={self.allow_partial})")

    def process(self, audio_frame: np.ndarray) -> bool:
        if not self._initialized or self.rec is None:
            return False

        # Cooldown: evita re-trigger inmediato después de detección
        if time.time() - self._last_detection_time < self.cooldown_seconds:
            return False

        audio_bytes = audio_frame.tobytes()
        is_final = self.rec.AcceptWaveform(audio_bytes)

        if is_final:
            # Resultado final
            final_result = json.loads(self.rec.Result())
            final_text = final_result.get("text", "").lower().strip()
            if final_text:
                self._last_final = final_text
                logger.info(f"[VoskWakeWord] Final: '{final_text}'")
                if self._keyword_in_text(final_text):
                    logger.info(f"[VoskWakeWord] ✅ DETECTED in final: '{final_text}'")
                    self._last_detection_time = time.time()
                    self._last_partial = ""
                    return True
        else:
            # Resultado parcial (solo usamos si allow_partial=True)
            partial_result = json.loads(self.rec.PartialResult())
            partial_text = partial_result.get("partial", "").lower().strip()

            if partial_text and partial_text != self._last_partial:
                self._last_partial = partial_text
                logger.debug(f"[VoskWakeWord] Partial: '{partial_text}'")

            # Solo disparar en partial si está explícitamente habilitado y el texto
            # es exactamente la keyword (más estricto, menos falsos positivos)
            if self.allow_partial and partial_text:
                words = partial_text.split()
                if len(words) <= 2 and self._keyword_in_text(partial_text):
                    logger.info(f"[VoskWakeWord] ✅ DETECTED in partial: '{partial_text}'")
                    self._last_detection_time = time.time()
                    self._last_partial = ""
                    return True

        return False

    def _keyword_in_text(self, text: str) -> bool:
        if not text:
            return False
        keyword = self.keyword.lower().strip()
        if keyword in text:
            for plural_suffix in ['s', 'es', 'ed']:
                plural = keyword + plural_suffix
                if plural in text:
                    return False
            return True
        return False

    def reset(self):
        """Reinicia el recognizer para una nueva sesión de escucha."""
        if self.model is None:
            return
        try:
            from vosk import KaldiRecognizer
            self.rec = KaldiRecognizer(self.model, self.sample_rate)
            self._last_partial = ""
            self._last_final = ""
        except Exception as e:
            logger.error(f"[VoskWakeWord] Reset error: {e}")

    def is_initialized(self) -> bool:
        return self._initialized

    def cleanup(self):
        self._initialized = False
        self.rec = None
        self.model = None
