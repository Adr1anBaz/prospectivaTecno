import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from prospectiva.bus.event_bus import EventBus
from prospectiva.procesos.orquestador import Orquestador
from prospectiva.modulos.stt.groq_stt import GroqSTT
from prospectiva.modulos.llm.groq_llm import GroqLLM
from prospectiva.modulos.tts.deepgram_tts import DeepgramTTS
from prospectiva.modulos.classifier.configurable_classifier import ConfigurableClassifier
from prospectiva.modulos.muta.vosk_wakeword import VoskWakeWord


def test_e2e_mock():
    """Test E2E flow with mock data injected manually."""
    print("=" * 60)
    print("TEST E2E - Online Flow (Architecture Test)")
    print("=" * 60)

    bus = EventBus()
    test_queue = mp.Queue()
    bus.set_broadcast_queues([test_queue])
    bus.set_private_queue(test_queue)

    # Create components (will fail on API calls but that's expected without keys)
    stt = GroqSTT(api_key="test")
    llm = GroqLLM(api_key="test")
    tts = DeepgramTTS(api_key="test")
    classifier = ConfigurableClassifier(config_path="config/commands.yaml")

    system_prompt = "Eres un asistente universitario."
    orquestador = Orquestador(bus, stt, llm, tts, classifier, system_prompt)

    # Test 1: Simulate WAKE_WORD_DETECTED
    print("\n[TEST 1] Wake word detection")
    bus.publish("WAKE_WORD_DETECTED", {"timestamp": 0.0})
    evt = bus.get(timeout=1)
    assert evt[0] == "WAKE_WORD_DETECTED"
    print("✅ Wake word event captured")

    # Test 2: Simulate SPEECH_COMPLETED
    print("\n[TEST 2] Speech completed -> transcription")
    import numpy as np
    fake_audio = np.zeros(16000, dtype=np.int16).tobytes()
    bus.publish("SPEECH_COMPLETED", {"audio": fake_audio, "sample_rate": 16000})

    evt = bus.get(timeout=1)
    assert evt[0] == "SPEECH_COMPLETED"
    print("✅ Speech completed event captured")

    # Test 3: Classifier
    print("\n[TEST 3] Intent classification")
    tests = [
        ("llévame a biomédica", "NAVEGAR_BIOMEDICA"),
        ("voy al giornale", "NAVEGAR_GIORNALE"),
        ("siéntate", "COMANDO_SIT"),
        ("baila", "COMANDO_DANCE"),
        ("hola qué tal", "COMANDO_WAVE"),
    ]
    for text, expected in tests:
        intent, meta = classifier.classify(text)
        assert intent.value == expected, f"Expected {expected}, got {intent.value}"
        print(f"  '{text}' -> {intent.value} ✅")

    # Test 4: VoskWakeWord (offline)
    print("\n[TEST 4] VoskWakeWord initialization")
    vosk_model_path = os.path.abspath("models/vosk/vosk-model-small-es-0.42")
    if os.path.exists(vosk_model_path):
        wake_word = VoskWakeWord(model_path=vosk_model_path, keyword="oye robot")
        wake_word.initialize()
        assert wake_word.is_initialized()
        print("✅ VoskWakeWord initialized successfully")
        wake_word.cleanup()
    else:
        print("⚠️  Vosk model not found, skipping. Run: uv run python scripts/download_vosk_model.py")

    # Test 5: EventBus broadcast
    print("\n[TEST 5] EventBus broadcast")
    bus.publish("A", 1)
    bus.publish("B", 2)
    time.sleep(0.1)
    evt1 = bus.get(timeout=0.5)
    evt2 = bus.get(timeout=0.5)
    assert evt1 is not None and evt1[0] == "A"
    assert evt2 is not None and evt2[0] == "B"
    print(f"✅ Events received: {evt1[0]}, {evt2[0]}")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)
    print("\nTo run the full assistant with real APIs:")
    print("  1. Copy .env.example to .env")
    print("  2. Add your GROQ_API_KEY and DEEPGRAM_API_KEY")
    print("  3. Run: uv run python src/prospectiva/main.py")

if __name__ == "__main__":
    import multiprocessing as mp
    test_e2e_mock()
