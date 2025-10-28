import os
from typing import List, Optional
from openai import OpenAI
from .models import ChatMessage, ChatRequest, ChatResponse

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found. Please set it in your .env file or environment variables.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def generate_response(self, request: ChatRequest) -> ChatResponse:
        if not self.is_available():
            raise Exception("OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Be friendly, informative, and concise in your responses."}
        ]
        
        for msg in request.conversation_history:
            messages.append({"role": msg.role, "content": msg.content})
        
        messages.append({"role": "user", "content": request.message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            updated_history = request.conversation_history.copy()
            updated_history.append(ChatMessage(role="user", content=request.message))
            updated_history.append(ChatMessage(role="assistant", content=assistant_response))
            
            return ChatResponse(
                response=assistant_response,
                conversation_history=updated_history
            )
            
        except Exception as e:
            raise Exception(f"Error processing chat request: {str(e)}")

openai_service = OpenAIService()
