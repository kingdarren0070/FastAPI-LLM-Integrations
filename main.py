from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from dotenv import load_dotenv

from app.models import ChatRequest, ChatResponse
from app.services import openai_service

load_dotenv()

app = FastAPI(
    title="FastAPI Chatbot Project",
    description="A FastAPI application with OpenAI-powered chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/landing.html")

@app.get("/chatbot")
async def chatbot():
    return FileResponse("static/index.html")


@app.get("/api")
async def api_info():
    return {"message": "Welcome to FastAPI Chatbot API!", "version": "1.0.0"}


@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    try:
        if not openai_service.is_available():
            raise HTTPException(
                status_code=503, 
                detail="Create a .env file and set your OpenAI API key"
            )
        
        return openai_service.generate_response(request)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
