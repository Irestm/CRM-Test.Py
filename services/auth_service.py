from schemas.auth import UserCreate, UserResponse, Token
from infrastructure.uow import UnitOfWork
from domain.user import User
from core.security import hash_password, verify_password, create_access_token

async def register_user(user_data: UserCreate, uow: UnitOfWork) -> UserResponse:
    async with uow:
        existing_user = await uow.users.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
            
        hashed_pwd = hash_password(user_data.password)
        new_user = User(email=user_data.email, hashed_password=hashed_pwd)
        added_user = await uow.users.add(new_user)
        await uow.commit()
        return UserResponse(id=added_user.id, email=added_user.email)

async def login_user(user_data: UserCreate, uow: UnitOfWork) -> Token:
    async with uow:
        user = await uow.users.get_by_email(user_data.email)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise ValueError("Invalid credentials")
            
        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")