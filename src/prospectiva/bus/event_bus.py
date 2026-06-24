import multiprocessing as mp
import queue
from typing import Any
import logging

logger = logging.getLogger(__name__)

class EventBus:
    """
    Process-safe event bus. publish() broadcasts to ALL known queues.
    Each process reads from its own private queue via get().
    """

    def __init__(self, known_queues: list[mp.Queue] | None = None):
        # All queues to broadcast to when publishing
        self._broadcast_queues: list[mp.Queue] = known_queues or []
        # This process's private queue for reading
        self._private_queue: mp.Queue = mp.Queue()
        # Also keep a default queue for backward compat (single-process tests)
        self._default_queue: mp.Queue = mp.Queue()

    def set_broadcast_queues(self, queues: list[mp.Queue]):
        """Set all queues for broadcasting (called in main process)."""
        self._broadcast_queues = queues

    def set_private_queue(self, q: mp.Queue):
        """Set the private queue for this process (called in child process)."""
        self._private_queue = q

    def publish(self, event_type: str, payload: Any):
        """Publish event to ALL known queues."""
        for q in self._broadcast_queues:
            q.put((event_type, payload))
        # Also put on default queue for backward compat
        self._default_queue.put((event_type, payload))
        logger.debug(f"[EventBus] Published: {event_type} to {len(self._broadcast_queues)} queue(s)")

    def get(self, timeout: float | None = None) -> tuple[str, Any] | None:
        """Get next event from this process's private queue."""
        try:
            return self._private_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    @property
    def queue(self) -> mp.Queue:
        """Backward compat: access the private queue directly."""
        return self._private_queue

    def drain(self) -> list[tuple[str, Any]]:
        """Drain all pending events from all queues."""
        events = []
        for q in self._broadcast_queues + [self._default_queue, self._private_queue]:
            try:
                while True:
                    events.append(q.get_nowait())
            except queue.Empty:
                pass
        return events