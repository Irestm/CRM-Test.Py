from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus
from services import task_service
from infrastructure.uow import UnitOfWork
from src.api.dependencies import get_uow
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

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    deleted = await task_service.delete_task(task_id, current_user.id, uow)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or already deleted")

@router.post("/{task_id}/upload", response_model=TaskResponse)
async def upload_file(
    task_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    task = await task_service.upload_file_to_task(task_id, current_user.id, file, uow)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or deleted")
    return task