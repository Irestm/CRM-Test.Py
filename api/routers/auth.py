from fastapi import APIRouter, Depends, HTTPException, status
from schemas.auth import UserCreate, UserResponse, Token
from services import auth_service
from infrastructure.uow import UnitOfWork
from src.api.dependencies import get_uow

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        return await auth_service.register_user(user_data, uow)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=Token)
async def login(user_data: UserCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        return await auth_service.login_user(user_data, uow)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))