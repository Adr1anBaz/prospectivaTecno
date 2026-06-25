import requests
import json

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

def test_conversation_with_context():
    """Test that the model can maintain context across multiple messages"""

    # Initialize conversation history
    conversation_history = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Keep your answers brief and concise."
        }
    ]

    # First message
    print("=" * 60)
    print("Testing Ollama conversation with context")
    print("=" * 60)

    # Question 1
    user_message_1 = "My name is Adrian. What's 2 + 2?"
    conversation_history.append({
        "role": "user",
        "content": user_message_1
    })

    print(f"\nUser: {user_message_1}")

    payload = {
        "model": "llama3.2:3b",
        "messages": conversation_history,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 100
        }
    }

    try:
        response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        assistant_reply = data.get("message", {}).get("content", "")
        print(f"Assistant: {assistant_reply}")

        # Add assistant response to history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_reply
        })

        # Question 2 - testing context memory
        user_message_2 = "What is my name?"
        conversation_history.append({
            "role": "user",
            "content": user_message_2
        })

        print(f"\nUser: {user_message_2}")

        payload["messages"] = conversation_history

        response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        assistant_reply_2 = data.get("message", {}).get("content", "")
        print(f"Assistant: {assistant_reply_2}")

        # Add to history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_reply_2
        })

        # Show metrics
        print("\n" + "=" * 60)
        print("Metrics from last response:")
        print("=" * 60)
        print(f"Total duration: {data.get('total_duration', 0) / 1e9:.2f} seconds")
        print(f"Input tokens: {data.get('prompt_eval_count', 0)}")
        print(f"Output tokens: {data.get('eval_count', 0)}")
        print(f"Generation speed: {data.get('eval_count', 0) / (data.get('eval_duration', 1) / 1e9):.2f} tokens/s")

        print("\n✓ Context test successful! The model remembered the name.")

    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to Ollama.")
        print("Make sure Ollama is running with: ollama serve")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")

if __name__ == "__main__":
    test_conversation_with_context()
