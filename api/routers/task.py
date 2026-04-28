from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
import os

from schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus
from schemas.audit_log import AuditLogResponse
from schemas.task_file import TaskFileResponse
from services import task_service
from infrastructure.uow import UnitOfWork
from api.dependencies import get_uow
from api.dependencies_auth import get_current_user
from domain.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
        task_data: TaskCreate,
        current_user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    return await task_service.create_task(task_data, current_user.id, uow)


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
        status: Optional[str] = None,
        current_user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    return await task_service.list_tasks(current_user.id, uow, include_deleted=False, status=status)


@router.get("/deleted", response_model=List[TaskResponse])
async def list_deleted_tasks(
        current_user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    return await task_service.list_tasks(current_user.id, uow, include_deleted=True)


@router.delete("/deleted/empty", status_code=status.HTTP_204_NO_CONTENT)
async def empty_deleted_tasks(
        current_user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    await task_service.empty_trash(current_user.id, uow)


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
        task_id: int,
        status_data: TaskUpdateStatus,
        current_user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    task = await task_service.update_task_status(task_id, current_user.id, status_data, uow)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or deleted")
    return task


@router.patch("/{task_id}/restore", response_model=TaskResponse)
async def restore_task(
        task_id: int,
        current_user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    restored = await task_service.restore_task(task_id, current_user.id, uow)
    if not restored:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not in trash")

    async with uow:
        task = await uow.tasks.get(task_id)
        return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        current_user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    deleted = await task_service.delete_task(task_id, current_user.id, uow)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or already deleted")


@router.post("/{task_id}/files", response_model=List[TaskFileResponse])
async def upload_task_files(
        task_id: int,
        files: List[UploadFile],
        current_user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    uploaded_files = await task_service.upload_files_to_task(task_id, current_user.id, files, uow)
    if not uploaded_files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or user not authorized")
    return uploaded_files


@router.get("/{task_id}/audit", response_model=List[AuditLogResponse])
async def get_task_audit_log(
        task_id: int,
        current_user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    audit_logs = await task_service.get_task_audit_logs(task_id, current_user.id, uow)
    if not audit_logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or user not authorized")
    return audit_logs


@router.get("/{task_id}/pdf")
async def generate_task_pdf(task_id: int):
    dummy_pdf_path = "dummy.pdf"
    with open(dummy_pdf_path, "wb") as f:
        f.write(
            b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<</ProcSet[/PDF/Text]/Font<</F1 5 0 R>>>>/Contents 4 0 R>>endobj 4 0 obj<</Length 55>>stream\nBT /F1 24 Tf 100 700 Td (Hello, this is a dummy PDF!) Tj ET\nendstream 5 0 obj<</Type/Font/Subtype/Type1/Name/F1/BaseFont/Helvetica/Encoding/MacRomanEncoding>>endobj\nxref\n0 6\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000125 00000 n\n0000000301 00000 n\n0000000390 00000 n\ntrailer<</Size 6/Root 1 0 R>>startxref\n490\n%%EOF")
    return FileResponse(path=dummy_pdf_path, filename=f"task_{task_id}_proposal.pdf", media_type="application/pdf")