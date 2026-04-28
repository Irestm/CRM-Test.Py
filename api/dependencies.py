from core.database import AsyncSessionLocal
from infrastructure.uow import SqlAlchemyUnitOfWork

def get_uow() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(AsyncSessionLocal)
