from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

from domain.task import Task
from domain.task_file import TaskFile
from domain.audit_log import AuditLog
from services.task_service import TaskService
from database import get_db # Assuming a database.py exists with get_db

router = APIRouter()

UPLOAD_DIRECTORY = "uploads" # This should be configured properly, e.g., in settings

@router.post("/tasks/{task_id}/files")
async def upload_task_files(task_id: int, files: List[UploadFile], db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    uploaded_files_info = []

    for file in files:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
        
        task_file = TaskFile(task_id=task_id, file_path=file_location, file_name=file.filename)
        db.add(task_file)
        uploaded_files_info.append({"filename": file.filename, "location": file_location})
    
    db.commit()
    return {"message": "Files uploaded successfully", "files": uploaded_files_info}

@router.get("/tasks/{task_id}/audit")
def get_task_audit_log(task_id: int, db: Session = Depends(get_db)):
    audit_logs = db.query(AuditLog).filter(AuditLog.task_id == task_id).all()
    return audit_logs

@router.get("/tasks/{task_id}/pdf")
def generate_task_pdf(task_id: int):
    # This is a placeholder. In a real application, you would generate a PDF here.
    # For now, it returns a dummy file.
    dummy_pdf_path = "dummy.pdf"
    with open(dummy_pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<</ProcSet[/PDF/Text]/Font<</F1 5 0 R>>>>/Contents 4 0 R>>endobj 4 0 obj<</Length 55>>stream\nBT /F1 24 Tf 100 700 Td (Hello, this is a dummy PDF!) Tj ET\nendstream 5 0 obj<</Type/Font/Subtype/Type1/Name/F1/BaseFont/Helvetica/Encoding/MacRomanEncoding>>endobj\nxref\n0 6\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000125 00000 n\n0000000301 00000 n\n0000000390 00000 n\ntrailer<</Size 6/Root 1 0 R>>startxref\n490\n%%EOF")
    return FileResponse(path=dummy_pdf_path, filename=f"task_{task_id}_proposal.pdf", media_type="application/pdf")
