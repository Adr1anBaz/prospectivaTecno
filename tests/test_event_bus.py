import os
import sys
import multiprocessing as mp
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from prospectiva.bus.event_bus import EventBus


def _publisher(cons_q, ver_q):
    """Publish 3 events to consumer queue."""
    b = EventBus()
    b.set_broadcast_queues([cons_q])  # Only send to consumer
    b.set_private_queue(cons_q)
    b.publish("TEST_EVENT_1", {"msg": "hello"})
    time.sleep(0.1)
    b.publish("TEST_EVENT_2", {"msg": "world"})
    time.sleep(0.1)
    b.publish("DONE", {})


def _consumer(cons_q, ver_q):
    """Consume 3 events, then publish VERIFY on ver_q."""
    b = EventBus()
    b.set_broadcast_queues([ver_q])  # Only send VERIFY to verifier
    b.set_private_queue(cons_q)
    events = []
    while True:
        event = b.get(timeout=2.0)
        if event is None:
            break
        event_type, payload = event
        events.append(event_type)
        if event_type == "DONE":
            break
    print(f"  Consumer received: {events}")
    b.publish("VERIFY", {"passed": True, "count": len(events)})
    print(f"  Consumer published VERIFY")


def test_event_bus_cross_process():
    """Test that EventBus works correctly across spawn processes."""
    print("=" * 60)
    print("TEST EVENT BUS CROSS-PROCESS")
    print("=" * 60)
    
    mp.set_start_method("spawn", force=True)

    cons_q = mp.Queue()
    ver_q = mp.Queue()

    p1 = mp.Process(target=_publisher, args=(cons_q, ver_q))
    p2 = mp.Process(target=_consumer, args=(cons_q, ver_q))
    p1.start()
    p2.start()
    p1.join(timeout=5)
    p2.join(timeout=5)

    if p1.is_alive():
        p1.terminate()
        p1.join()
    if p2.is_alive():
        p2.terminate()
        p2.join()

    import queue as qlib
    try:
        event_type, payload = ver_q.get(timeout=1.0)
        print(f"  Verifier got: {event_type}")
        assert event_type == "VERIFY"
        assert payload["passed"] == True
        print(f"✅ EventBus works across processes ({payload['count']} events)")
    except qlib.Empty:
        print("❌ EventBus test failed - no VERIFY event received")
        return False

    print("\n" + "=" * 60)
    print("TEST PASSED")
    print("=" * 60)
    return True


if __name__ == "__main__":
    test_event_bus_cross_process()
