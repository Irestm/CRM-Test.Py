from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from infrastructure.repository import ClientRepository, SqlAlchemyClientRepository
from infrastructure.repository_auth import UserRepository, SqlAlchemyUserRepository
from infrastructure.repository_task import TaskRepository, SqlAlchemyTaskRepository

class UnitOfWork(Protocol):
    clients: ClientRepository
    users: UserRepository
    tasks: TaskRepository
    
    async def __aenter__(self) -> 'UnitOfWork':
        ...
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...
        
    async def commit(self):
        ...
        
    async def rollback(self):
        ...

class SqlAlchemyUnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.clients = SqlAlchemyClientRepository(self.session)
        self.users = SqlAlchemyUserRepository(self.session)
        self.tasks = SqlAlchemyTaskRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()