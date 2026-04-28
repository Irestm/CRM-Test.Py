from typing import Protocol, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from domain.task import Task as TaskDomain
from infrastructure.orm import TaskModel

class TaskRepository(Protocol):
    async def add(self, task: TaskDomain) -> TaskDomain:
        ...
        
    async def get(self, task_id: int) -> Optional[TaskDomain]:
        ...
        
    async def list_by_user(self, user_id: int, include_deleted: bool = False, status: Optional[str] = None) -> List[TaskDomain]:
        ...
        
    async def update(self, task: TaskDomain) -> TaskDomain:
        ...
        
    async def delete_all_trashed_by_user(self, user_id: int) -> None:
        ...

class SqlAlchemyTaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, task: TaskDomain) -> TaskDomain:
        db_task = TaskModel(
            title=task.title,
            description=task.description,
            status=task.status,
            file_path=task.file_path,
            comment=task.comment,
            user_id=task.user_id,
            is_deleted=task.is_deleted
        )
        self.session.add(db_task)
        await self.session.flush()
        task.id = db_task.id
        return task

    async def get(self, task_id: int) -> Optional[TaskDomain]:
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        result = await self.session.execute(stmt)
        db_task = result.scalar_one_or_none()
        if db_task:
            return TaskDomain(
                id=db_task.id, title=db_task.title, description=db_task.description,
                status=db_task.status, file_path=db_task.file_path, comment=db_task.comment,
                user_id=db_task.user_id, is_deleted=db_task.is_deleted
            )
        return None

    async def list_by_user(self, user_id: int, include_deleted: bool = False, status: Optional[str] = None) -> List[TaskDomain]:
        stmt = select(TaskModel).where(TaskModel.user_id == user_id)
        
        if include_deleted:
            stmt = stmt.where(TaskModel.is_deleted == True)
        else:
            stmt = stmt.where(TaskModel.is_deleted == False)
            
        if status:
            stmt = stmt.where(TaskModel.status == status)
            
        result = await self.session.execute(stmt)
        return [
            TaskDomain(
                id=t.id, title=t.title, description=t.description,
                status=t.status, file_path=t.file_path, comment=t.comment,
                user_id=t.user_id, is_deleted=t.is_deleted
            ) for t in result.scalars()
        ]

    async def update(self, task: TaskDomain) -> TaskDomain:
        stmt = update(TaskModel).where(TaskModel.id == task.id).values(
            title=task.title,
            description=task.description,
            status=task.status,
            file_path=task.file_path,
            comment=task.comment,
            is_deleted=task.is_deleted
        )
        await self.session.execute(stmt)
        return task
        
    async def delete_all_trashed_by_user(self, user_id: int) -> None:
        stmt = delete(TaskModel).where(TaskModel.user_id == user_id, TaskModel.is_deleted == True)
        await self.session.execute(stmt)