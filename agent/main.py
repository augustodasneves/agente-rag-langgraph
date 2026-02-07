import uvicorn
import logging
from fastapi import FastAPI
from agent.api.routes import router
from agent.config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    """Application factory for the RAG Agent."""
    app = FastAPI(
        title="RAG Agent Pro",
        description="A production-ready RAG Agent built with LangGraph and Ollama",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(router)
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "agent.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True
    )
