import os
import uuid
from typing import List, Optional
from fastapi import UploadFile
from schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus
from infrastructure.uow import UnitOfWork
from domain.task import Task
from services.pdf_parser import extract_text_from_pdf

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def create_task(task_data: TaskCreate, user_id: int, uow: UnitOfWork) -> TaskResponse:
    async with uow:
        new_task = Task(
            title=task_data.title, 
            description=task_data.description, 
            task_type=task_data.task_type,
            company_name=task_data.company_name,
            amount=task_data.amount,
            user_id=user_id
        )
        added_task = await uow.tasks.add(new_task)
        await uow.commit()
        return TaskResponse.model_validate(added_task)

async def list_tasks(user_id: int, uow: UnitOfWork, include_deleted: bool = False, status: Optional[str] = None) -> List[TaskResponse]:
    async with uow:
        tasks = await uow.tasks.list_by_user(user_id, include_deleted, status)
        return [TaskResponse.model_validate(t) for t in tasks]

async def update_task_status(task_id: int, user_id: int, status_data: TaskUpdateStatus, uow: UnitOfWork) -> Optional[TaskResponse]:
    async with uow:
        task = await uow.tasks.get(task_id)
        if not task or task.user_id != user_id or task.is_deleted:
            return None
            
        task.status = status_data.status
        if status_data.comment:
            task.comment = status_data.comment
            
        updated_task = await uow.tasks.update(task)
        await uow.commit()
        return TaskResponse.model_validate(updated_task)

async def delete_task(task_id: int, user_id: int, uow: UnitOfWork) -> bool:
    async with uow:
        task = await uow.tasks.get(task_id)
        if not task or task.user_id != user_id or task.is_deleted:
            return False
            
        task.is_deleted = True
        await uow.tasks.update(task)
        await uow.commit()
        return True

async def restore_task(task_id: int, user_id: int, uow: UnitOfWork) -> bool:
    async with uow:
        task = await uow.tasks.get(task_id)
        if not task or task.user_id != user_id or not task.is_deleted:
            return False
            
        task.is_deleted = False
        await uow.tasks.update(task)
        await uow.commit()
        return True

async def empty_trash(user_id: int, uow: UnitOfWork) -> None:
    async with uow:
        await uow.tasks.delete_all_trashed_by_user(user_id)
        await uow.commit()

async def upload_file_to_task(task_id: int, user_id: int, file: UploadFile, uow: UnitOfWork) -> Optional[TaskResponse]:
    async with uow:
        task = await uow.tasks.get(task_id)
        if not task or task.user_id != user_id or task.is_deleted:
            return None
            
        file_ext = file.filename.split(".")[-1] if file.filename else "bin"
        file_name = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        file_bytes = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)
            
        if file_ext.lower() == "pdf":
            parsed_text = await extract_text_from_pdf(file_bytes)
            task.description = (task.description or "") + "\n\n[Parsed Content]:\n" + parsed_text

        task.file_path = file_path
        updated_task = await uow.tasks.update(task)
        await uow.commit()
        return TaskResponse.model_validate(updated_task)