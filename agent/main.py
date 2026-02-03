from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from agent.graph import app_graph
from agent.ingestion import ingest_pdfs
import shutil
import os

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    inputs = {"question": query.question}
    result = await app_graph.ainvoke(inputs)
    return {"answer": result["answer"]}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not os.path.exists("data"):
        os.makedirs("data")
    
    file_path = os.path.join("data", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Trigger ingestion only for the new file
    ingest_pdfs(file_path)
    
    return {"message": f"File {file.filename} uploaded and ingested successfully."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
