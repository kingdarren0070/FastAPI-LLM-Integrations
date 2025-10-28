"""
Services for handling OpenAI API interactions and business logic.
"""

import os
from typing import List, Optional
from openai import OpenAI
from .models import ChatMessage, ChatRequest, ChatResponse


class OpenAIService:
    """Service class for handling OpenAI API interactions."""
    
    def __init__(self):
        """Initialize the OpenAI service with API key."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found. Please set it in your .env file or environment variables.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available."""
        return self.client is not None
    
    def generate_response(self, request: ChatRequest) -> ChatResponse:
        """
        Generate a response using OpenAI API.
        
        Args:
            request: ChatRequest containing message and conversation history
            
        Returns:
            ChatResponse with generated response and updated conversation history
            
        Raises:
            Exception: If OpenAI API call fails or service is unavailable
        """
        if not self.is_available():
            raise Exception("OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")
        
        # Prepare conversation history for OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Be friendly, informative, and concise in your responses."}
        ]
        
        # Add conversation history
        for msg in request.conversation_history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": request.message})
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            # Get the assistant's response
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            updated_history = request.conversation_history.copy()
            updated_history.append(ChatMessage(role="user", content=request.message))
            updated_history.append(ChatMessage(role="assistant", content=assistant_response))
            
            return ChatResponse(
                response=assistant_response,
                conversation_history=updated_history
            )
            
        except Exception as e:
            raise Exception(f"Error processing chat request: {str(e)}")


# Global service instance
openai_service = OpenAIService()
