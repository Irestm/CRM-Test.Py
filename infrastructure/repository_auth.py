from typing import Protocol, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.user import User as UserDomain
from infrastructure.orm import UserModel

class UserRepository(Protocol):
    async def add(self, user: UserDomain) -> UserDomain:
        ...
        
    async def get_by_email(self, email: str) -> Optional[UserDomain]:
        ...
        
    async def get_by_id(self, user_id: int) -> Optional[UserDomain]:
        ...

class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: UserDomain) -> UserDomain:
        db_user = UserModel(email=user.email, hashed_password=user.hashed_password)
        self.session.add(db_user)
        await self.session.flush()
        user.id = db_user.id
        return user

    async def get_by_email(self, email: str) -> Optional[UserDomain]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user:
            return UserDomain(id=db_user.id, email=db_user.email, hashed_password=db_user.hashed_password)
        return None
        
    async def get_by_id(self, user_id: int) -> Optional[UserDomain]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user:
            return UserDomain(id=db_user.id, email=db_user.email, hashed_password=db_user.hashed_password)
        return None