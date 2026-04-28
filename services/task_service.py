import os
import uuid
from typing import List, Optional
from fastapi import UploadFile
from schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus
from infrastructure.uow import UnitOfWork
from domain.task import Task
from domain.audit_log import AuditLog
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
            user_id=user_id,
            client_id=task_data.client_id # Add client_id here
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
        
        original_status = task.status
        original_amount = task.amount

        task.status = status_data.status
        if status_data.comment:
            task.comment = status_data.comment
        
        # Assuming amount can also be updated via this endpoint or another one
        # For now, only status change is explicitly handled for audit log here.
        # If amount is updated, you'd add a similar check.
        
        if original_status != task.status:
            audit_description = f"Status changed from '{original_status}' to '{task.status}'"
            audit_log = AuditLog(task_id=task.id, user_id=user_id, action="TASK_STATUS_UPDATE", description=audit_description)
            uow.session.add(audit_log) # Assuming uow.session gives access to the SQLAlchemy session

        updated_task = await uow.tasks.update(task)
        await uow.commit()
        return TaskResponse.model_validate(updated_task)

async def delete_task(task_id: int, user_id: int, uow: UnitOfWork) -> bool:
    async with uow:
        task = await uow.tasks.get(task_id)
        if not task or task.user_id != user_id or task.is_deleted:
            return False
            
        task.is_deleted = True
        audit_log = AuditLog(task_id=task.id, user_id=user_id, action="TASK_DELETED", description="Task marked as deleted")
        uow.session.add(audit_log)
        await uow.tasks.update(task)
        await uow.commit()
        return True

async def restore_task(task_id: int, user_id: int, uow: UnitOfWork) -> bool:
    async with uow:
        task = await uow.tasks.get(task_id)
        if not task or task.user_id != user_id or not task.is_deleted:
            return False
            
        task.is_deleted = False
        audit_log = AuditLog(task_id=task.id, user_id=user_id, action="TASK_RESTORED", description="Task restored from trash")
        uow.session.add(audit_log)
        await uow.tasks.update(task)
        await uow.commit()
        return True

async def empty_trash(user_id: int, uow: UnitOfWork) -> None:
    async with uow:
        # This operation might delete multiple tasks, so logging each deletion might be too verbose.
        # A single log for emptying trash might be more appropriate, or detailed logging within the repository.
        await uow.tasks.delete_all_trashed_by_user(user_id)
        await uow.commit()

# Removed upload_file_to_task as it's replaced by the new endpoint
