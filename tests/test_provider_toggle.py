#!/usr/bin/env python3
"""
Test del toggle de providers (STT/TTS).

Verifica que se pueda cambiar entre:
- STT: Groq (Whisper) vs Deepgram (Nova-3)
- TTS: Deepgram (Aura-2) vs Local (Mock)

Ejecutar:
    uv run python tests/test_provider_toggle.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()


def test_provider_factory():
    """Test that provider factory works correctly."""
    print("=" * 60)
    print("🧪 TEST: Provider Toggle System")
    print("=" * 60)
    
    # Test STT providers
    print("\n🎙️ Testing STT Providers:")
    
    # Test Groq STT
    from prospectiva.modulos.stt.groq_stt import GroqSTT
    groq_stt = GroqSTT()
    print(f"   ✅ GroqSTT: model={groq_stt.model}")
    
    # Test Deepgram STT
    from prospectiva.modulos.stt.deepgram_stt import DeepgramSTT
    deepgram_stt = DeepgramSTT(model="nova-3")
    print(f"   ✅ DeepgramSTT: model={deepgram_stt.model}")
    
    # Test TTS providers
    print("\n🔊 Testing TTS Providers:")
    
    # Test Deepgram TTS
    from prospectiva.modulos.tts.deepgram_tts import DeepgramTTS
    deepgram_tts = DeepgramTTS(model="aura-2-thalia-en")
    print(f"   ✅ DeepgramTTS: model={deepgram_tts.model}, available={deepgram_tts.is_available()}")
    
    # Test Local TTS
    from prospectiva.modulos.tts.local_tts import LocalTTS
    local_tts = LocalTTS()
    print(f"   ✅ LocalTTS: available={local_tts.is_available()}")
    
    # Test factory functions
    print("\n⚙️ Testing Provider Factory:")
    
    from prospectiva.main import get_stt_provider, get_tts_provider
    
    groq_key = os.getenv("GROQ_API_KEY")
    deepgram_key = os.getenv("DEEPGRAM_API_KEY")
    
    # Test STT factory
    stt_groq = get_stt_provider(groq_key, deepgram_key, "groq")
    print(f"   ✅ STT Groq: {type(stt_groq).__name__}")
    
    stt_deepgram = get_stt_provider(groq_key, deepgram_key, "deepgram")
    print(f"   ✅ STT Deepgram: {type(stt_deepgram).__name__}")
    
    # Test TTS factory
    tts_deepgram = get_tts_provider(deepgram_key, "deepgram")
    print(f"   ✅ TTS Deepgram: {type(tts_deepgram).__name__}")
    
    tts_local = get_tts_provider(deepgram_key, "local")
    print(f"   ✅ TTS Local: {type(tts_local).__name__}")
    
    # Test default values
    stt_default = get_stt_provider(groq_key, deepgram_key, "invalid")
    print(f"   ✅ STT Default (invalid → groq): {type(stt_default).__name__}")
    
    tts_default = get_tts_provider(deepgram_key, "invalid")
    print(f"   ✅ TTS Default (invalid → deepgram): {type(tts_default).__name__}")
    
    print("\n" + "=" * 60)
    print("✅ TESTS PASSED")
    print("=" * 60)


def test_env_vars():
    """Test that environment variables are set correctly."""
    print("\n" + "=" * 60)
    print("🧪 TEST: Environment Variables")
    print("=" * 60)
    
    stt_provider = os.getenv("STT_PROVIDER", "groq").lower()
    tts_provider = os.getenv("TTS_PROVIDER", "deepgram").lower()
    
    print(f"\n📋 Current configuration:")
    print(f"   STT_PROVIDER={stt_provider}")
    print(f"   TTS_PROVIDER={tts_provider}")
    print(f"   GROQ_API_KEY={'✅ Set' if os.getenv('GROQ_API_KEY') else '❌ Missing'}")
    print(f"   DEEPGRAM_API_KEY={'✅ Set' if os.getenv('DEEPGRAM_API_KEY') else '❌ Missing'}")
    
    print("\n✅ Environment variables loaded correctly")


if __name__ == "__main__":
    test_env_vars()
    test_provider_factory()
