#!/usr/bin/env python3
"""
Simple test script for the FastAPI chatbot
Run this after starting the server to test the chatbot functionality
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_chatbot():
    """Test the chatbot functionality"""
    print("🤖 Testing FastAPI Chatbot")
    print("=" * 50)
    
    # Test messages
    test_messages = [
        "Hello! How are you?",
        "What's the weather like today?",
        "Can you help me write a Python function?",
        "Tell me a joke!"
    ]
    
    conversation_history = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: {message}")
        print("-" * 30)
        
        try:
            # Send message to chatbot
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
                print(f"🤖 Bot: {data['response']}")
                conversation_history = data['conversation_history']
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to server. Make sure the server is running on http://localhost:8000")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Small delay between messages
        time.sleep(1)
    
    print("\n✅ Chatbot test completed!")

def test_health():
    """Test the health endpoint"""
    print("\n🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    print("Starting FastAPI Chatbot Tests")
    print("Make sure the server is running: python main.py")
    print()
    
    # Test health first
    test_health()
    
    # Test chatbot
    test_chatbot()

