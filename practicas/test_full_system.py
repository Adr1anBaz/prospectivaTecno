#!/usr/bin/env python3
"""
Test script to verify the full chatbot system is working.
This tests the backend API endpoint.
"""

import requests
import json

BACKEND_URL = "http://localhost:8000/chat"

def test_chatbot_system():
    print("=" * 70)
    print("TESTING FULL CHATBOT SYSTEM")
    print("=" * 70)

    # Test 1: Simple question
    print("\n📝 Test 1: Basic question about sensors")
    print("-" * 70)

    payload1 = {
        "message": "¿Qué es un sensor ultrasónico? Responde en máximo 50 palabras.",
        "model": "llama3.2:3b",
        "temperature": 0.7,
        "top_p": 0.9,
        "num_predict": 80,
        "num_ctx": 4096,
        "repeat_penalty": 1.1
    }

    try:
        response = requests.post(BACKEND_URL, json=payload1, timeout=60)
        response.raise_for_status()
        data = response.json()

        print(f"\n👤 Usuario: {payload1['message']}")
        print(f"\n🤖 Modelo ({data['model']}): {data['reply']}")

        metrics = data['metrics']
        print(f"\n📊 Métricas:")
        print(f"   • Tiempo total: {metrics['total_duration_s']:.3f}s")
        print(f"   • Tokens entrada: {metrics['prompt_eval_count']}")
        print(f"   • Tokens salida: {metrics['eval_count']}")
        print(f"   • Velocidad: {metrics['tokens_per_second']:.2f} tokens/s")

        # Test 2: Technical question
        print("\n" + "=" * 70)
        print("\n📝 Test 2: Technical question with different parameters")
        print("-" * 70)

        payload2 = {
            "message": "Dame un ejemplo muy breve de código Arduino para HC-SR04",
            "model": "llama3.2:3b",
            "temperature": 0.3,  # Lower temperature for code
            "top_p": 0.9,
            "num_predict": 150,
            "num_ctx": 4096,
            "repeat_penalty": 1.2
        }

        response = requests.post(BACKEND_URL, json=payload2, timeout=60)
        response.raise_for_status()
        data = response.json()

        print(f"\n👤 Usuario: {payload2['message']}")
        print(f"\n🤖 Modelo ({data['model']}): {data['reply'][:200]}...")

        metrics = data['metrics']
        print(f"\n📊 Métricas:")
        print(f"   • Tiempo total: {metrics['total_duration_s']:.3f}s")
        print(f"   • Tokens entrada: {metrics['prompt_eval_count']}")
        print(f"   • Tokens salida: {metrics['eval_count']}")
        print(f"   • Velocidad: {metrics['tokens_per_second']:.2f} tokens/s")

        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\n📌 The chatbot system is working correctly!")
        print("📌 Frontend available at: http://localhost:5500")
        print("📌 Backend API at: http://localhost:8000")
        print("📌 API docs at: http://localhost:8000/docs")
        print("\n🚀 You can now open the frontend in your browser!")

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to backend.")
        print("   Make sure the backend server is running:")
        print("   cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_chatbot_system()
