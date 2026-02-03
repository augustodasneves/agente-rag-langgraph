import os
from langchain_postgres.vectorstores import PGVector
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/rag_db")
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
collection_name = "pdf_documents"

def get_vector_store():
    embeddings = OllamaEmbeddings(
        model=os.getenv("LLM_MODEL", "llama3.2"),
        base_url=ollama_base_url
    )
    
    vector_store = PGVector(
        connection=connection_string,
        embeddings=embeddings,
        collection_name=collection_name,
        use_jsonb=True,
    )
    return vector_store
