from typing import List
from langchain_postgres.vectorstores import PGVector
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from agent.config.settings import settings
from agent.core.interfaces import IVectorStoreProvider

class PostgresVectorStore(IVectorStoreProvider):
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )
        self.vector_store = PGVector(
            connection=settings.DATABASE_URL,
            embeddings=self.embeddings,
            collection_name=settings.VECTOR_COLLECTION_NAME,
            use_jsonb=True,
        )

    def add_documents(self, documents: List[Document]) -> None:
        self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        return self.vector_store.similarity_search(query, k=k)

# Singleton instance for the application
vector_store_service = PostgresVectorStore()
