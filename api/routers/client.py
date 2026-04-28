from typing import List
from fastapi import APIRouter, Depends, HTTPException
from schemas.client import ClientCreate, ClientResponse
from services import client_service
from infrastructure.uow import UnitOfWork
from api.dependencies import get_uow

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientResponse)
async def create_client(client_data: ClientCreate, uow: UnitOfWork = Depends(get_uow)):
    return await client_service.create_client(client_data, uow)

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(client_id: int, uow: UnitOfWork = Depends(get_uow)):
    client = await client_service.get_client(client_id, uow)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/", response_model=List[ClientResponse])
async def list_clients(uow: UnitOfWork = Depends(get_uow)):
    return await client_service.list_clients(uow)
