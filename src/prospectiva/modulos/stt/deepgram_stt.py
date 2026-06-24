import os
import time
import logging
import threading
import queue
from io import BytesIO
from typing import Optional
from prospectiva.interfaces.stt import SpeechToText
from prospectiva.utils.audio_utils import preprocess_audio

logger = logging.getLogger(__name__)

class DeepgramSTT(SpeechToText):
    """
    Speech-to-Text usando Deepgram Streaming (Nova-3).

    Conecta via WebSocket a Deepgram para transcripción en tiempo real.
    Más rápido y preciso que Whisper para español.

    Usage:
        stt = DeepgramSTT(api_key=...)
        stt.start()
        stt.send_audio(chunk_bytes)
        text = stt.get_transcription()
        stt.stop()
    """

    def __init__(self, api_key: str | None = None, model: str = "nova-3", language: str = "es"):
        from deepgram import DeepgramClient
        self.api_key = api_key or os.getenv("DEEPGRAM_API_KEY")
        self.client = DeepgramClient(api_key=self.api_key)
        self.model = model
        self.language = language
        self.connection = None
        self._transcription_queue = queue.Queue()
        self._final_transcripts = []
        self._running = False
        self._connected = threading.Event()
        self._lock = threading.Lock()
        logger.info(f"[DeepgramSTT] Initialized with model={model}, lang={language}")

    def start(self):
        """Start the WebSocket connection to Deepgram."""
        if self._running:
            return True

        try:
            self._final_transcripts = []
            self._connected.clear()

            # Connect to Deepgram streaming with Nova-3
            self.connection = self.client.listen.v1.connect(
                model=self.model,
                language=self.language,
                smart_format=True,
                interim_results=True,
                encoding="linear16",
                sample_rate=16000,
                channels=1,
                endpointing=300,  # 300ms of silence = end of utterance
            )

            # Register event handlers
            self.connection.on("open", self._on_open)
            self.connection.on("message", self._on_message)
            self.connection.on("close", self._on_close)
            self.connection.on("error", self._on_error)

            # Start listening in background thread
            self._listen_thread = threading.Thread(target=self._listen, daemon=True)
            self._listen_thread.start()

            # Wait for connection to be ready (max 5s)
            if not self._connected.wait(timeout=5.0):
                logger.error("[DeepgramSTT] Connection timeout")
                self.stop()
                return False

            self._running = True
            logger.info("[DeepgramSTT] WebSocket connection started")
            return True
        except Exception as e:
            logger.error(f"[DeepgramSTT] Failed to start: {e}")
            return False

    def stop(self):
        """Stop the WebSocket connection."""
        self._running = False
        self._connected.clear()
        if self.connection:
            try:
                self.connection.finish()
            except Exception as e:
                logger.warning(f"[DeepgramSTT] Error finishing connection: {e}")

        if hasattr(self, '_listen_thread') and self._listen_thread.is_alive():
            self._listen_thread.join(timeout=5.0)

        logger.info("[DeepgramSTT] Stopped")

    def send_audio(self, audio_bytes: bytes):
        """Send audio chunk to Deepgram for real-time transcription."""
        if not self._running or not self.connection:
            logger.warning("[DeepgramSTT] Not running, cannot send audio")
            return

        try:
            self.connection.send(audio_bytes)
        except Exception as e:
            logger.warning(f"[DeepgramSTT] Error sending audio: {e}")

    def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        """
        Synchronous transcription interface.

        Streams audio to Deepgram in chunks and returns final transcription.
        """
        if not audio_bytes or len(audio_bytes) < 3200:  # ~0.1s minimum
            logger.warning("[DeepgramSTT] Audio too short, ignoring")
            return ""

        # Preprocess audio
        try:
            processed_bytes = preprocess_audio(
                audio_bytes,
                sample_rate=sample_rate,
                normalize=True,
                trim_silence_flag=True,
                target_db=-20.0,
            )
        except Exception as e:
            logger.warning(f"[DeepgramSTT] Preprocessing failed, using raw audio: {e}")
            processed_bytes = audio_bytes

        # Start connection (or restart if not running)
        if not self._running:
            if not self.start():
                logger.error("[DeepgramSTT] Could not start connection")
                return ""

        # Clear any previous transcripts
        while not self._transcription_queue.empty():
            try:
                self._transcription_queue.get_nowait()
            except queue.Empty:
                break

        # Send audio in chunks (100ms each = 3200 bytes @ 16kHz mono int16)
        chunk_size = 3200
        total = len(processed_bytes)
        logger.info(f"[DeepgramSTT] Sending {total} bytes in {total // chunk_size + 1} chunks")

        for i in range(0, total, chunk_size):
            chunk = processed_bytes[i:i + chunk_size]
            self.send_audio(chunk)
            time.sleep(0.05)  # ~20 chunks/sec to simulate real-time streaming

        # Tell Deepgram we're done with this utterance
        try:
            if self.connection:
                self.connection.finish()
        except Exception as e:
            logger.warning(f"[DeepgramSTT] Error finishing utterance: {e}")

        # Wait for final transcript
        final_text = ""
        deadline = time.time() + 8.0  # 8 second timeout for this utterance
        last_partial = ""

        while time.time() < deadline:
            try:
                transcript = self._transcription_queue.get(timeout=0.5)
                if transcript:
                    final_text = transcript
                    logger.info(f"[DeepgramSTT] Final transcript so far: '{final_text}'")
                    # If we got a final transcript and it's been stable, return it
                    if transcript == last_partial and len(transcript) > 0:
                        break
                    last_partial = transcript
            except queue.Empty:
                # No more transcripts coming
                if final_text:
                    break

        if not final_text:
            logger.warning("[DeepgramSTT] No transcription received (timeout)")

        # Restart connection for next utterance
        self.stop()

        return final_text

    def get_transcription(self, timeout: float = 5.0) -> str:
        """Get the latest transcription from the queue."""
        try:
            return self._transcription_queue.get(timeout=timeout)
        except queue.Empty:
            return ""

    def _listen(self):
        """Background thread to listen for Deepgram responses."""
        try:
            self.connection.start()
        except Exception as e:
            logger.error(f"[DeepgramSTT] Listening error: {e}")

    def _on_open(self, _):
        logger.info("[DeepgramSTT] WebSocket connection opened")
        self._connected.set()

    def _on_message(self, message):
        try:
            # Extract transcript from message
            if hasattr(message, 'channel') and hasattr(message.channel, 'alternatives'):
                transcript = message.channel.alternatives[0].transcript
                if transcript:
                    is_final = getattr(message.channel, 'is_final', False)
                    logger.debug(f"[DeepgramSTT] {'Final' if is_final else 'Interim'}: '{transcript}'")
                    if is_final:
                        logger.info(f"[DeepgramSTT] Transcript: {transcript}")
                        self._transcription_queue.put(transcript)
        except Exception as e:
            logger.warning(f"[DeepgramSTT] Error parsing message: {e}")

    def _on_close(self, _):
        logger.info("[DeepgramSTT] WebSocket connection closed")
        self._running = False
        self._connected.clear()

    def _on_error(self, error):
        logger.error(f"[DeepgramSTT] WebSocket error: {error}")
        self._connected.set()  # Unblock wait even on error

    def is_available(self) -> bool:
        return self._running
