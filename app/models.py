"""
Pydantic models for the FastAPI chatbot application.
"""

from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    """Represents a single message in a conversation."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    conversation_history: List[ChatMessage]
