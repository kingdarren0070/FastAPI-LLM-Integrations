# FastAPI Chatbot

A simple OpenAI-powered chatbot with a beautiful web interface built with FastAPI.

## Features

- 🤖 **OpenAI GPT-4o** integration
- 💬 **Web Interface** - Beautiful, responsive chat UI
- 🔄 **Conversation History** - Maintains context
- 📱 **Mobile Friendly** - Works on all devices

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key:**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Open your browser:**
   - Go to http://localhost:8000
   - Click "OpenAI GPT-4o" to start chatting

## API Usage

**Chat with the bot:**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello!", "conversation_history": []}'
```

**API Documentation:**
- http://localhost:8000/docs - Interactive API docs
- http://localhost:8000/health - Health check
