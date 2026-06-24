import os
import sys
import multiprocessing as mp
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from prospectiva.bus.event_bus import EventBus


def event_consumer(bus):
    """Consume events and log them."""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    
    logger.info("[Consumer] Started")
    event_count = 0
    while True:
        try:
            event = bus.get(timeout=1.0)
            if event is None:
                logger.info("[Consumer] No event (timeout)")
                continue
            event_type, payload = event
            event_count += 1
            logger.info(f"[Consumer] Event #{event_count}: {event_type}")
            
            if event_type == "SPEECH_COMPLETED":
                logger.info("[Consumer] Processing SPEECH_COMPLETED...")
                time.sleep(0.5)
                text = "Llévame a Biomédica"
                logger.info(f"[Consumer] STT result: '{text}'")
                logger.info("[Consumer] Publishing TEXT_TRANSCRIBED")
                bus.publish("TEXT_TRANSCRIBED", {"text": text})
                
            elif event_type == "TEXT_TRANSCRIBED":
                logger.info(f"[Consumer] Processing TEXT_TRANSCRIBED: '{payload.get('text', '')}'")
                
            elif event_type == "STOP":
                logger.info("[Consumer] Stopping")
                break
        except Exception as e:
            logger.error(f"[Consumer] Error: {e}")
    
    logger.info("[Consumer] Stopped")


def test_event_consumer():
    """Test event consumer with real logging."""
    print("=" * 60)
    print("TEST EVENT CONSUMER")
    print("=" * 60)
    
    mp.set_start_method("spawn", force=True)
    bus = EventBus()
    
    # Start consumer
    p = mp.Process(target=event_consumer, args=(bus,))
    p.start()
    
    # Publish events
    time.sleep(0.5)
    bus.publish("WAKE_WORD_DETECTED", {"timestamp": time.time()})
    time.sleep(0.5)
    bus.publish("SPEECH_COMPLETED", {"audio": b"fake_speech", "sample_rate": 16000})
    
    # Wait for processing
    time.sleep(3.0)
    
    # Stop
    bus.publish("STOP", {})
    
    p.join(timeout=5)
    if p.is_alive():
        p.terminate()
        p.join()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_event_consumer()
