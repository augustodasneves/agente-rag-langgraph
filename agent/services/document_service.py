import os
import logging
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from agent.config.settings import settings
from agent.services.vector_store import vector_store_service

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self, vector_store=vector_store_service):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )

    def process_pdf(self, file_path: str) -> bool:
        try:
            if not os.path.exists(file_path) or not file_path.endswith(".pdf"):
                logger.warning(f"Invalid file path: {file_path}")
                return False

            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            chunks = self.text_splitter.split_documents(documents)
            if not chunks:
                logger.warning(f"No content extracted from: {file_path}")
                return False

            self.vector_store.add_documents(chunks)
            logger.info(f"Successfully ingested {os.path.basename(file_path)}: {len(chunks)} chunks.")
            return True
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            return False

document_service = DocumentService()
