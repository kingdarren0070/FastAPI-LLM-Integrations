import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_chatbot():
    print("Testing FastAPI Chatbot")
    print("=" * 50)
    
    test_messages = [
        "Hello! How are you?",
        "What's the weather like today?",
        "Can you help me write a Python function?",
        "Tell me a joke!"
    ]
    
    conversation_history = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: {message}")
        print("-" * 30)
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={
                    "message": message,
                    "conversation_history": conversation_history
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Bot: {data['response']}")
                conversation_history = data['conversation_history']
            else:
                print(f"Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to server. Make sure the server is running on http://localhost:8000")
            break
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(1)
    
    print("\nChatbot test completed!")

if __name__ == "__main__":
    print("Starting FastAPI Chatbot Tests")
    print("Make sure the server is running: python main.py")
    print()
    test_chatbot()

