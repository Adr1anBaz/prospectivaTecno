import os
import sys
import multiprocessing as mp
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from prospectiva.bus.event_bus import EventBus


def orquestador_spawn_test(bus):
    """Test orquestador in spawn process."""
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    
    logger.info("[OrquestadorSpawn] Started")
    event_count = 0
    while True:
        try:
            event = bus.get(timeout=1.0)
            if event is None:
                logger.debug("[OrquestadorSpawn] No event (timeout)")
                continue
            event_type, payload = event
            event_count += 1
            logger.info(f"[OrquestadorSpawn] Event #{event_count}: {event_type}")
            
            if event_type == "SPEECH_COMPLETED":
                logger.info("[OrquestadorSpawn] Processing SPEECH_COMPLETED...")
                time.sleep(0.5)
                text = "Llévame a Biomédica"
                logger.info(f"[OrquestadorSpawn] STT result: '{text}'")
                logger.info("[OrquestadorSpawn] Publishing TEXT_TRANSCRIBED")
                bus.publish("TEXT_TRANSCRIBED", {"text": text})
                
            elif event_type == "TEXT_TRANSCRIBED":
                logger.info(f"[OrquestadorSpawn] Processing TEXT_TRANSCRIBED: '{payload.get('text', '')}'")
                logger.info("[OrquestadorSpawn] Publishing AUDIO_SYNTHESIZED")
                bus.publish("AUDIO_SYNTHESIZED", {"audio": b"fake_audio"})
                
            elif event_type == "AUDIO_SYNTHESIZED":
                logger.info(f"[OrquestadorSpawn] Audio synthesized: {len(payload.get('audio', b''))} bytes")
                
            elif event_type == "STOP":
                logger.info("[OrquestadorSpawn] Stopping")
                break
        except Exception as e:
            logger.error(f"[OrquestadorSpawn] Error: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    logger.info("[OrquestadorSpawn] Stopped")


def test_orquestador_spawn():
    """Test orquestador in spawn process."""
    print("=" * 60)
    print("TEST ORQUESTADOR SPAWN")
    print("=" * 60)
    
    mp.set_start_method("spawn", force=True)
    bus = EventBus()
    
    # Start orquestador in spawn process
    p = mp.Process(target=orquestador_spawn_test, args=(bus,))
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
    test_orquestador_spawn()
