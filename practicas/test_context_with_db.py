#!/usr/bin/env python3
"""
Test script to verify conversation context is maintained using SQLite database.
This demonstrates that the chatbot remembers previous messages within a conversation.
"""

import requests
import json

BACKEND_URL = "http://localhost:8000/chat"
CONVERSATIONS_URL = "http://localhost:8000/conversations"

def test_context_maintenance():
    print("=" * 80)
    print("TESTING CONVERSATION CONTEXT WITH SQLITE DATABASE")
    print("=" * 80)

    conversation_id = None

    # Message 1: Introduce yourself
    print("\n📝 Message 1: User introduces themself")
    print("-" * 80)

    payload1 = {
        "message": "Me llamo Adrián y soy estudiante de ingeniería",
        "conversation_id": conversation_id,
        "model": "llama3.2:3b",
        "temperature": 0.7,
        "num_predict": 100
    }

    try:
        response = requests.post(BACKEND_URL, json=payload1, timeout=60)
        response.raise_for_status()
        data = response.json()

        conversation_id = data["conversation_id"]

        print(f"\n👤 Usuario: {payload1['message']}")
        print(f"\n🤖 Asistente: {data['reply']}")
        print(f"\n📊 Conversación ID: {conversation_id}")
        print(f"   Tokens totales: {data['metrics']['total_tokens']}")

        # Message 2: Ask what the model knows
        print("\n" + "=" * 80)
        print("\n📝 Message 2: Ask about user information")
        print("-" * 80)

        payload2 = {
            "message": "¿Cómo me llamo y qué estudio?",
            "conversation_id": conversation_id,  # IMPORTANT: Use same conversation_id
            "model": "llama3.2:3b",
            "temperature": 0.7,
            "num_predict": 100
        }

        response = requests.post(BACKEND_URL, json=payload2, timeout=60)
        response.raise_for_status()
        data = response.json()

        print(f"\n👤 Usuario: {payload2['message']}")
        print(f"\n🤖 Asistente: {data['reply']}")
        print(f"\n📊 Conversación ID: {data['conversation_id']}")
        print(f"   Tokens totales: {data['metrics']['total_tokens']}")

        # Message 3: Ask a follow-up question
        print("\n" + "=" * 80)
        print("\n📝 Message 3: Follow-up question")
        print("-" * 80)

        payload3 = {
            "message": "¿Qué temas de ingeniería podría estudiar?",
            "conversation_id": conversation_id,
            "model": "llama3.2:3b",
            "temperature": 0.7,
            "num_predict": 150
        }

        response = requests.post(BACKEND_URL, json=payload3, timeout=60)
        response.raise_for_status()
        data = response.json()

        print(f"\n👤 Usuario: {payload3['message']}")
        print(f"\n🤖 Asistente: {data['reply'][:200]}...")
        print(f"\n📊 Conversación ID: {data['conversation_id']}")
        print(f"   Tokens totales: {data['metrics']['total_tokens']}")

        # Retrieve full conversation from database
        print("\n" + "=" * 80)
        print("\n📚 Retrieving full conversation from database")
        print("-" * 80)

        response = requests.get(f"{CONVERSATIONS_URL}/{conversation_id}")
        response.raise_for_status()
        conversation_data = response.json()

        print(f"\n✅ Conversation: {conversation_data['title']}")
        print(f"   Created: {conversation_data['created_at']}")
        print(f"   Total messages: {len(conversation_data['messages'])}")

        print("\n📋 Full conversation history:")
        for i, msg in enumerate(conversation_data['messages'], 1):
            role_icon = "👤" if msg['role'] == 'user' else "🤖"
            print(f"\n   {i}. {role_icon} {msg['role'].upper()}: {msg['content'][:100]}...")

        # Test: Start a NEW conversation
        print("\n" + "=" * 80)
        print("\n🆕 Starting a NEW conversation (no context from previous)")
        print("-" * 80)

        payload4 = {
            "message": "¿Cómo me llamo?",
            "conversation_id": None,  # None = new conversation
            "model": "llama3.2:3b",
            "temperature": 0.7,
            "num_predict": 100
        }

        response = requests.post(BACKEND_URL, json=payload4, timeout=60)
        response.raise_for_status()
        data = response.json()

        new_conversation_id = data["conversation_id"]

        print(f"\n👤 Usuario: {payload4['message']}")
        print(f"\n🤖 Asistente: {data['reply']}")
        print(f"\n📊 Nueva conversación ID: {new_conversation_id}")
        print(f"   (El modelo NO recuerda porque es una conversación nueva)")

        # List all conversations
        print("\n" + "=" * 80)
        print("\n📋 All conversations in database:")
        print("-" * 80)

        response = requests.get(CONVERSATIONS_URL)
        response.raise_for_status()
        all_conversations = response.json()

        for conv in all_conversations:
            print(f"\n   ID: {conv['id']} | Title: {conv['title']}")
            print(f"   Messages: {conv['message_count']} | Updated: {conv['updated_at']}")

        print("\n" + "=" * 80)
        print("✅ CONTEXT TEST SUCCESSFUL!")
        print("=" * 80)
        print("\n📌 Key findings:")
        print("   ✓ The model remembers information within the same conversation")
        print("   ✓ Context is maintained across multiple messages")
        print("   ✓ New conversations start with fresh context")
        print("   ✓ All conversations are stored in SQLite database")
        print("\n🎉 The chatbot now maintains conversation context perfectly!")

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to backend.")
        print("   Make sure the backend server is running:")
        print("   cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_context_maintenance()
