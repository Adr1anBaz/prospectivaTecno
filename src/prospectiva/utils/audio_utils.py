"""
Audio preprocessing utilities for STT.

Provides normalization, silence trimming, and WAV packaging
to improve transcription quality.
"""

import io
import wave
import logging
import numpy as np

logger = logging.getLogger(__name__)


def int16_to_float(audio: np.ndarray) -> np.ndarray:
    """Convert int16 PCM to float32 in [-1, 1]."""
    if audio.dtype == np.float32 or audio.dtype == np.float64:
        return audio.astype(np.float32)
    return audio.astype(np.float32) / 32768.0


def float_to_int16(audio: np.ndarray) -> np.ndarray:
    """Convert float32 in [-1, 1] to int16 PCM."""
    audio = np.clip(audio, -1.0, 1.0)
    return (audio * 32767.0).astype(np.int16)


def normalize_audio(audio: np.ndarray, target_db: float = -20.0) -> np.ndarray:
    """
    Normalize audio to target RMS level (in dBFS).
    
    Args:
        audio: Audio samples (int16 or float)
        target_db: Target RMS level in dBFS (negative). -20 is a good level for speech.
    """
    audio_float = int16_to_float(audio)
    
    # Calculate RMS
    rms = np.sqrt(np.mean(audio_float ** 2))
    if rms < 1e-10:
        return audio_float
    
    # Current dB
    current_db = 20 * np.log10(rms)
    
    # Gain needed
    gain_db = target_db - current_db
    gain = 10 ** (gain_db / 20)
    
    # Apply gain and clip
    normalized = np.clip(audio_float * gain, -1.0, 1.0)
    
    logger.debug(
        f"[AudioUtils] Normalized from {current_db:.1f}dB to {target_db:.1f}dB "
        f"(gain={gain:.2f})"
    )
    
    return normalized


def trim_silence(
    audio: np.ndarray,
    sample_rate: int = 16000,
    threshold_db: float = -40.0,
    min_silence_ms: int = 200,
    keep_ms: int = 100,
) -> np.ndarray:
    """
    Trim leading and trailing silence from audio.
    
    Args:
        audio: Audio samples
        sample_rate: Sample rate in Hz
        threshold_db: Silence threshold in dBFS
        min_silence_ms: Minimum silence duration to trim (ms)
        keep_ms: Amount of audio to keep around speech (ms)
    """
    audio_float = int16_to_float(audio)
    
    if len(audio_float) == 0:
        return audio_float
    
    # Convert threshold to linear
    threshold = 10 ** (threshold_db / 20)
    
    # Frame-level energy (20ms frames)
    frame_size = int(sample_rate * 0.02)
    if frame_size == 0 or len(audio_float) < frame_size:
        return audio_float
    
    frames = []
    for i in range(0, len(audio_float) - frame_size + 1, frame_size):
        frame = audio_float[i:i + frame_size]
        rms = np.sqrt(np.mean(frame ** 2))
        frames.append(rms > threshold)
    
    if not frames:
        return audio_float
    
    # Find first and last non-silent frame
    frames = np.array(frames)
    speech_indices = np.where(frames)[0]
    
    if len(speech_indices) == 0:
        logger.debug("[AudioUtils] No speech found, returning original audio")
        return audio_float
    
    first_frame = speech_indices[0]
    last_frame = speech_indices[-1]
    
    # Convert to samples
    keep_samples = int(sample_rate * keep_ms / 1000)
    first_sample = max(0, first_frame * frame_size - keep_samples)
    last_sample = min(len(audio_float), (last_frame + 1) * frame_size + keep_samples)
    
    trimmed = audio_float[first_sample:last_sample]
    
    logger.debug(
        f"[AudioUtils] Trimmed silence: {len(audio_float)} -> {len(trimmed)} samples "
        f"({len(audio_float) / sample_rate:.2f}s -> {len(trimmed) / sample_rate:.2f}s)"
    )
    
    return trimmed


def preprocess_audio(
    audio_bytes: bytes,
    sample_rate: int = 16000,
    normalize: bool = True,
    trim_silence_flag: bool = True,
    target_db: float = -20.0,
) -> bytes:
    """
    Preprocess raw PCM audio bytes for STT.
    
    Returns raw int16 PCM bytes.
    """
    # Convert bytes to numpy
    audio = np.frombuffer(audio_bytes, dtype=np.int16)
    
    if len(audio) == 0:
        return audio_bytes
    
    # Trim silence first
    if trim_silence_flag:
        audio = trim_silence(audio, sample_rate=sample_rate)
    
    # Normalize
    if normalize:
        audio = normalize_audio(audio, target_db=target_db)
        audio = float_to_int16(audio)
    
    return audio.tobytes()


def pcm_to_wav_bytes(audio_bytes: bytes, sample_rate: int = 16000, channels: int = 1) -> bytes:
    """Convert raw PCM bytes to WAV bytes."""
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_bytes)
    wav_buffer.seek(0)
    return wav_buffer.read()


def get_audio_stats(audio_bytes: bytes, sample_rate: int = 16000) -> dict:
    """Get audio statistics for debugging."""
    audio = np.frombuffer(audio_bytes, dtype=np.int16)
    if len(audio) == 0:
        return {"duration": 0, "rms_db": -np.inf, "peak": 0}
    
    audio_float = int16_to_float(audio)
    rms = np.sqrt(np.mean(audio_float ** 2))
    rms_db = 20 * np.log10(rms) if rms > 1e-10 else -np.inf
    peak = np.max(np.abs(audio_float))
    duration = len(audio) / sample_rate
    
    return {
        "duration": duration,
        "rms_db": rms_db,
        "peak": peak,
        "samples": len(audio),
    }
