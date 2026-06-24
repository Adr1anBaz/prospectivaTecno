import os
import sys
import multiprocessing as mp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from prospectiva.bus.event_bus import EventBus


# ---------------------------------------------------------------------------
# Worker functions (must be at module level for pickling)
# ---------------------------------------------------------------------------

def check_bus_worker(bus):
    """Test that EventBus works in a spawn process."""
    evt = bus.get(timeout=1)
    assert evt[0] == "TEST"
    bus.publish("RESULT", {"ok": True})


def audio_worker(bus, vosk_path):
    """Test Vosk initialization in a spawn process."""
    from prospectiva.modulos.muta.vosk_wakeword import VoskWakeWord
    import numpy as np

    wake_word = VoskWakeWord(model_path=vosk_path, keyword="oye robot")
    wake_word.initialize()

    fake_audio = np.zeros(512, dtype=np.int16)
    result = wake_word.process(fake_audio)

    bus.publish("AUDIO_TEST", {"initialized": wake_word.is_initialized(), "result": result})


def orquestador_worker(bus, groq_key, deepgram_key):
    """Test Groq/Deepgram initialization in a spawn process."""
    from prospectiva.modulos.stt.groq_stt import GroqSTT
    from prospectiva.modulos.llm.groq_llm import GroqLLM
    from prospectiva.modulos.tts.deepgram_tts import DeepgramTTS
    from prospectiva.modulos.classifier.regex_classifier import RegexIntentClassifier

    stt = GroqSTT(api_key=groq_key)
    llm = GroqLLM(api_key=groq_key)
    tts = DeepgramTTS(api_key=deepgram_key)
    classifier = RegexIntentClassifier()

    intent, meta = classifier.classify("llévame a biomédica")

    bus.publish("ORQUESTADOR_TEST", {
        "stt_initialized": True,
        "llm_initialized": True,
        "tts_available": tts.is_available(),
        "intent": intent.value,
    })


def playback_worker(bus):
    """Test AudioPlayback initialization in a spawn process."""
    from prospectiva.procesos.playback import AudioPlayback

    playback = AudioPlayback(bus)
    bus.publish("PLAYBACK_TEST", {"initialized": True})


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

def test_multiprocessing_spawn():
    """Test full multiprocessing with spawn."""
    print("=" * 60)
    print("TEST MULTIPROCESSING - SPAWN")
    print("=" * 60)

    mp.set_start_method("spawn", force=True)
    bus = EventBus()

    # Test 1: EventBus via spawn
    print("\n[TEST 1] EventBus via spawn process")
    bus.publish("TEST", {"msg": "hello"})
    p1 = mp.Process(target=check_bus_worker, args=(bus,))
    p1.start()
    p1.join(timeout=5)
    assert p1.exitcode == 0, f"Process failed with exitcode={p1.exitcode}"
    evt = bus.get(timeout=1)
    assert evt[1]["ok"] == True
    print("✅ EventBus passed to spawn process successfully")

    # Test 2: Audio worker in spawn process
    print("\n[TEST 2] Audio worker in spawn process")
    vosk_path = os.path.abspath("models/vosk/vosk-model-small-es-0.42")
    p2 = mp.Process(target=audio_worker, args=(bus, vosk_path))
    p2.start()
    p2.join(timeout=30)

    if p2.is_alive():
        p2.terminate()
        p2.join()
        print("❌ Audio worker timed out or hung")
    else:
        if p2.exitcode == 0:
            evt = bus.get(timeout=1)
            assert evt[0] == "AUDIO_TEST"
            assert evt[1]["initialized"] == True
            print(f"✅ Audio worker: initialized={evt[1]['initialized']}, result={evt[1]['result']}")
        else:
            print(f"❌ Audio worker failed with exitcode={p2.exitcode}")

    # Test 3: Orquestador worker in spawn process
    print("\n[TEST 3] Orquestador worker in spawn process")
    p3 = mp.Process(target=orquestador_worker, args=(bus, "test", "test"))
    p3.start()
    p3.join(timeout=30)

    if p3.is_alive():
        p3.terminate()
        p3.join()
        print("❌ Orquestador worker timed out or hung")
    else:
        if p3.exitcode == 0:
            evt = bus.get(timeout=1)
            assert evt[0] == "ORQUESTADOR_TEST"
            assert evt[1]["stt_initialized"] == True
            assert evt[1]["intent"] == "NAVEGAR_BIOMEDICA"
            print(f"✅ Orquestador worker: STT={evt[1]['stt_initialized']}, TTS={evt[1]['tts_available']}, intent={evt[1]['intent']}")
        else:
            print(f"❌ Orquestador worker failed with exitcode={p3.exitcode}")

    # Test 4: Playback worker in spawn process
    print("\n[TEST 4] Playback worker in spawn process")
    p4 = mp.Process(target=playback_worker, args=(bus,))
    p4.start()
    p4.join(timeout=10)

    if p4.is_alive():
        p4.terminate()
        p4.join()
        print("❌ Playback worker timed out or hung")
    else:
        if p4.exitcode == 0:
            evt = bus.get(timeout=1)
            assert evt[0] == "PLAYBACK_TEST"
            assert evt[1]["initialized"] == True
            print(f"✅ Playback worker: initialized={evt[1]['initialized']}")
        else:
            print(f"❌ Playback worker failed with exitcode={p4.exitcode}")

    print("\n" + "=" * 60)
    print("ALL MULTIPROCESSING TESTS PASSED")
    print("=" * 60)
    print("\nEl sistema está listo para ejecutarse con:")
    print("  uv run python src/prospectiva/main.py")


if __name__ == "__main__":
    test_multiprocessing_spawn()
