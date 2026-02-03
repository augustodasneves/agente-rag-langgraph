import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from agent.database import get_vector_store

def ingest_pdfs(file_path):
    vector_store = get_vector_store()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, 
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    
    if os.path.exists(file_path) and file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        chunks = text_splitter.split_documents(documents)
        if chunks:
            vector_store.add_documents(chunks)
            print(f"Ingested {os.path.basename(file_path)}: {len(chunks)} chunks added.")
        else:
            print(f"Warning: No text found in {file_path}.")

if __name__ == "__main__":
    ingest_pdfs()
