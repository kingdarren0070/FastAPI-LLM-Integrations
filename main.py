from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from dotenv import load_dotenv

# Import our custom modules
from app.models import ChatRequest, ChatResponse
from app.services import openai_service

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

@app.get("/")
async def read_root():
    return FileResponse("static/landing.html")

@app.get("/chatbot")
async def chatbot():
    return FileResponse("static/index.html")

# API info endpoint
@app.get("/api")
async def api_info():
    return {"message": "Welcome to FastAPI Chatbot API!", "version": "1.0.0"}


# Chatbot endpoints
@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """
    Handle chat requests by processing them through the OpenAI service.
    
    Args:
        request: ChatRequest containing message and conversation history
        
    Returns:
        ChatResponse with generated response and updated conversation history
        
    Raises:
        HTTPException: If service is unavailable or processing fails
    """
    try:
        # Check if OpenAI service is available
        if not openai_service.is_available():
            raise HTTPException(
                status_code=503, 
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        # Process the request through the service
        return openai_service.generate_response(request)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
