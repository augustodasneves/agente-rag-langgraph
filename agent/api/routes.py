import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from werkzeug.utils import secure_filename
from agent.config.settings import settings
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
    # 1. Validar extensão
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    # 2. Sanitizar nome do arquivo (Evita Path Traversal)
    filename = secure_filename(file.filename)
    if not filename:
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido.")

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    file_path = os.path.join(data_dir, filename)
    
    try:
        # 3. Validar tamanho do arquivo
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="Arquivo muito grande (Máximo 10MB).")
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        success = document_service.process_pdf(file_path)
        if not success:
            raise HTTPException(status_code=500, detail="Falha ao processar e indexar o PDF.")
            
        return {"message": f"Arquivo {filename} processado com sucesso."}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=f"Erro no upload: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
