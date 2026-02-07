from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Database Settings
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/rag_db")
    
    # Ollama Settings
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    LLM_MODEL: str = Field(default="llama3.2")
    
    # RAG Settings
    CHUNK_SIZE: int = Field(default=600)
    CHUNK_OVERLAP: int = Field(default=150)
    VECTOR_COLLECTION_NAME: str = Field(default="pdf_documents")
    RETRIEVAL_K: int = Field(default=10)
    
    # API Settings
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    
    # Security Settings
    MAX_UPLOAD_SIZE: int = Field(default=10 * 1024 * 1024)  # 10MB
    ALLOWED_ORIGINS: list[str] = Field(default=["*"])

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
