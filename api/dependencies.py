from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import async_session_factory
from infrastructure.uow import SqlAlchemyUnitOfWork
from src.infrastructure.backup.local_hdd import LocalHDDStorage
from src.services.backup_service import BackupService

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

def get_uow() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(async_session_factory)

def get_backup_service() -> BackupService:
    storage = LocalHDDStorage(backup_dir="./backups")
    return BackupService(storage=storage, db_path="./crm.db")