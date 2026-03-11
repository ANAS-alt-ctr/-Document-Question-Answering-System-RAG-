from fastapi import APIRouter, UploadFile, File
import os
import shutil
from app.schemas import QuestionRequest
from app.rag_service import process_document, ask_question

router = APIRouter()




@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.endswith((".pdf", ".txt")):
        return {"error": "Only PDF or TXT allowed"}

    content = await file.read()
    chunks = process_document(file.filename, content)

    return {
        "message": "Document uploaded and processed successfully",
        "total_chunks": chunks
    }


@router.post("/ask-document")
async def ask_document(request: QuestionRequest):

    answer = ask_question(request.question)

    return {"answer": answer}