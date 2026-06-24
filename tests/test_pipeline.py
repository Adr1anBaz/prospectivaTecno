import os
import sys
import multiprocessing as mp
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from prospectiva.bus.event_bus import EventBus


def orquestador_simulator(bus):
    """Simulate the Orquestador event loop."""
    event_count = 0
    while True:
        event = bus.get(timeout=1.0)
        if event is None:
            continue
        event_type, payload = event
        event_count += 1
        print(f"[OrquestadorSim] Event #{event_count}: {event_type}")
        
        if event_type == "SPEECH_COMPLETED":
            print("[OrquestadorSim] Processing SPEECH_COMPLETED...")
            # Simulate STT
            time.sleep(0.5)
            text = "Llévame a Biomédica"
            print(f"[OrquestadorSim] STT result: '{text}'")
            print("[OrquestadorSim] Publishing TEXT_TRANSCRIBED")
            bus.publish("TEXT_TRANSCRIBED", {"text": text})
            
        elif event_type == "TEXT_TRANSCRIBED":
            print(f"[OrquestadorSim] Processing TEXT_TRANSCRIBED: '{payload.get('text', '')}'")
            # Simulate intent classification
            print("[OrquestadorSim] Intent: NAVEGAR_BIOMEDICA")
            print("[OrquestadorSim] Publishing AUDIO_SYNTHESIZED")
            bus.publish("AUDIO_SYNTHESIZED", {"audio": b"fake_audio"})
            
        elif event_type == "AUDIO_SYNTHESIZED":
            print(f"[OrquestadorSim] Audio synthesized: {len(payload.get('audio', b''))} bytes")
            
        elif event_type == "STOP":
            print("[OrquestadorSim] Stopping")
            break


def test_full_pipeline():
    """Test the full pipeline event flow."""
    print("=" * 60)
    print("TEST FULL PIPELINE EVENT FLOW")
    print("=" * 60)
    
    mp.set_start_method("spawn", force=True)
    bus = EventBus()
    
    # Start orquestador
    p = mp.Process(target=orquestador_simulator, args=(bus,))
    p.start()
    
    # Simulate wake word
    time.sleep(0.5)
    bus.publish("WAKE_WORD_DETECTED", {"timestamp": time.time()})
    
    # Simulate speech
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
    test_full_pipeline()
