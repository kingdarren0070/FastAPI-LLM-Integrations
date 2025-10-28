from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI(
    title="FastAPI Chatbot Project",
    description="A FastAPI application with OpenAI-powered chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Warning: OPENAI_API_KEY not found. Please set it in your .env file or environment variables.")
    openai_client = None
else:
    openai_client = OpenAI(api_key=openai_api_key)

# Pydantic models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    conversation_history: List[ChatMessage]

# Root endpoint - serve the landing page
@app.get("/")
async def read_root():
    return FileResponse("static/landing.html")

# Chatbot endpoint - serve the chat interface
@app.get("/chatbot")
async def chatbot():
    return FileResponse("static/index.html")

# API info endpoint
@app.get("/api")
async def api_info():
    return {"message": "Welcome to FastAPI Chatbot API!", "version": "1.0.0"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Chatbot endpoints
@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    try:
        # Check if OpenAI client is available
        if not openai_client:
            raise HTTPException(
                status_code=503, 
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        # Prepare conversation history for OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Be friendly, informative, and concise in your responses."}
        ]
        
        # Add conversation history
        for msg in request.conversation_history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": request.message})
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
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
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
