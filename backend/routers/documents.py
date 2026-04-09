from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil

from services.rag_service import RAGService

router = APIRouter()
rag = RAGService()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QueryRequest(BaseModel):
    question: str
    doc_filter: str | None = None


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    allowed = {".pdf", ".txt", ".csv", ".xlsx"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    dest = os.path.join(UPLOAD_DIR, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        chunk_count = rag.ingest(dest, file.filename)
    except Exception as e:
        os.remove(dest)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    return {
        "filename": file.filename,
        "status": "indexed",
        "chunks": chunk_count,
        "size_bytes": os.path.getsize(dest),
    }


@router.post("/query")
def query_documents(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        result = rag.query(req.question, doc_filter=req.doc_filter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


@router.get("/list")
def list_documents():
    return rag.list_documents()
