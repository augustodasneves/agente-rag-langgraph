from abc import ABC, abstractmethod
from typing import List, Iterable
from langchain_core.documents import Document

class IVectorStoreProvider(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        pass

class IDocumentLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> List[Document]:
        pass
