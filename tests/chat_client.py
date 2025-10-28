import requests
import json
import sys

API_BASE_URL = "http://localhost:8000"

def chat_with_bot(message, conversation_history=None):
    if conversation_history is None:
        conversation_history = []
    
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
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to server. Make sure it's running on http://localhost:8000"}
    except Exception as e:
        return {"error": str(e)}

def interactive_chat():
    print("FastAPI Chatbot Client")
    print("=" * 40)
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print()
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            elif user_input.lower() == 'clear':
                conversation_history = []
                print("Conversation history cleared.")
                continue
            elif not user_input:
                continue
            
            print("Bot: ", end="", flush=True)
            result = chat_with_bot(user_input, conversation_history)
            
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(result['response'])
                conversation_history = result['conversation_history']
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

def single_message(message):
    result = chat_with_bot(message)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Bot: {result['response']}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        single_message(message)
    else:
        interactive_chat()
