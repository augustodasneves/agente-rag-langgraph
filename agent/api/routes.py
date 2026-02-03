import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from agent.graph.workflow import rag_app
from agent.services.document_service import document_service

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        inputs = {"question": request.question}
        result = await rag_app.ainvoke(inputs)
        return QueryResponse(answer=result["answer"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no agente: {str(e)}")

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    file_path = os.path.join(data_dir, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        success = document_service.process_pdf(file_path)
        if not success:
            raise HTTPException(status_code=500, detail="Falha ao processar e indexar o PDF.")
            
        return {"message": f"Arquivo {file.filename} processado com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no upload: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
