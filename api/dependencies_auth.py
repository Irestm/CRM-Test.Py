from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_access_token
from infrastructure.uow import UnitOfWork
from api.dependencies import get_uow
from domain.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), uow: UnitOfWork = Depends(get_uow)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
        
    async with uow:
        # Assuming we need to get user by id, adding method to repository or doing raw query
        # Since we only have get_by_email, let's implement get by ID in repo if missing, or adjust here
        user = await uow.users.get_by_id(int(user_id))
        if user is None:
            raise credentials_exception
        return user