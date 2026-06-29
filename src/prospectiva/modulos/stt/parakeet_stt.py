import os
import logging
import time
from typing import Optional

import numpy as np
import onnxruntime as ort

from prospectiva.interfaces.stt import SpeechToText

logger = logging.getLogger(__name__)


class ParakeetSTT(SpeechToText):
    DEFAULT_MODEL_DIR = "/home/rimuru/.local/share/com.pais.handy/models/parakeet-tdt-0.6b-v3-int8"
    BLANK_IDX = 8192
    MAX_VOCAB_LOGIT = 8193

    def __init__(self, model_dir: Optional[str] = None, providers: Optional[list] = None):
        self.model_dir = model_dir or os.getenv("PARAKEET_MODEL_DIR", self.DEFAULT_MODEL_DIR)

        available = ort.get_available_providers()
        if providers is None:
            if "CUDAExecutionProvider" in available:
                self.providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
            else:
                self.providers = ["CPUExecutionProvider"]
        else:
            self.providers = providers

        self._preprocessor: Optional[ort.InferenceSession] = None
        self._encoder: Optional[ort.InferenceSession] = None
        self._decoder: Optional[ort.InferenceSession] = None
        self._vocab: dict[int, str] = {}

        logger.info(f"[ParakeetSTT] Model dir: {self.model_dir}, providers: {self.providers}")

    def _ensure_loaded(self):
        if self._preprocessor is not None:
            return

        logger.info("[ParakeetSTT] Loading ONNX sessions...")
        start = time.time()

        self._preprocessor = ort.InferenceSession(
            os.path.join(self.model_dir, "nemo128.onnx"),
            providers=self.providers,
        )
        self._encoder = ort.InferenceSession(
            os.path.join(self.model_dir, "encoder-model.int8.onnx"),
            providers=self.providers,
        )
        self._decoder = ort.InferenceSession(
            os.path.join(self.model_dir, "decoder_joint-model.int8.onnx"),
            providers=self.providers,
        )

        vocab_path = os.path.join(self.model_dir, "vocab.txt")
        with open(vocab_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().rsplit(" ", 1)
                if len(parts) == 2:
                    token, idx = parts
                    self._vocab[int(idx)] = token

        elapsed = time.time() - start
        logger.info(f"[ParakeetSTT] Loaded {len(self._vocab)} vocab tokens in {elapsed:.2f}s")

    def _load_audio(self, audio_bytes: bytes, sample_rate: int) -> tuple[np.ndarray, int]:
        if not audio_bytes:
            return np.array([], dtype=np.float32), 16000

        audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)
        audio_float = audio_int16.astype(np.float32) / 32768.0

        if sample_rate != 16000:
            try:
                import torch
                import torchaudio.functional as F

                x = torch.from_numpy(audio_float).unsqueeze(0)
                x = F.resample(x, sample_rate, 16000)
                audio_float = x.squeeze(0).numpy()
            except Exception:
                try:
                    from scipy.signal import resample_poly

                    audio_float = resample_poly(audio_float, 16000, sample_rate)
                except Exception as e2:
                    logger.error(
                        f"[ParakeetSTT] Resample failed (need torchaudio or scipy): {e2}"
                    )
                    return np.array([], dtype=np.float32), 16000

        return audio_float, 16000

    def _decode(self, encoder_outputs: np.ndarray, encoded_length: np.ndarray) -> str:
        T = int(encoded_length[0])
        targets = [self.BLANK_IDX]

        states_before_1 = np.zeros((2, 1, 640), dtype=np.float32)
        states_before_2 = np.zeros((2, 1, 640), dtype=np.float32)
        prev_label = self.BLANK_IDX

        t = 0
        while t < T:
            encoder_slice = encoder_outputs[:, :, t:t + 1]
            target_array = np.array([[prev_label]], dtype=np.int32)
            target_length = np.array([1], dtype=np.int32)

            logits, _, states_after_1, states_after_2 = self._decoder.run(None, {
                "encoder_outputs": encoder_slice,
                "targets": target_array,
                "target_length": target_length,
                "input_states_1": states_before_1,
                "input_states_2": states_before_2,
            })

            k = int(np.argmax(logits[0, 0, 0, : self.MAX_VOCAB_LOGIT]))

            if k == self.BLANK_IDX:
                t += 1
            else:
                targets.append(k)
                prev_label = k
                states_before_1 = states_after_1
                states_before_2 = states_after_2

        return self._targets_to_text(targets)

    def _targets_to_text(self, targets: list[int]) -> str:
        tokens = []
        for idx in targets:
            if idx == self.BLANK_IDX:
                continue
            token = self._vocab.get(idx, "")
            if token.startswith("<") and token.endswith(">"):
                continue
            tokens.append(token)
        text = "".join(tokens).replace("▁", " ").strip()
        return text

    def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        if not audio_bytes or len(audio_bytes) < 3200:
            logger.warning("[ParakeetSTT] Audio too short, ignoring")
            return ""

        self._ensure_loaded()

        try:
            start = time.time()
            audio_float, _ = self._load_audio(audio_bytes, sample_rate)

            if len(audio_float) == 0:
                return ""

            waveforms = audio_float[np.newaxis, :].astype(np.float32)
            waveforms_lens = np.array([audio_float.shape[0]], dtype=np.int64)

            features, features_lens = self._preprocessor.run(None, {
                "waveforms": waveforms,
                "waveforms_lens": waveforms_lens,
            })

            encoder_outputs, encoded_lengths = self._encoder.run(None, {
                "audio_signal": features,
                "length": features_lens,
            })

            text = self._decode(encoder_outputs, encoded_lengths)
            elapsed = time.time() - start
            logger.info(f"[ParakeetSTT] Transcribed in {elapsed:.2f}s: '{text[:80]}...'")
            return text

        except Exception as e:
            logger.error(f"[ParakeetSTT] Transcription error: {e}")
            return ""
