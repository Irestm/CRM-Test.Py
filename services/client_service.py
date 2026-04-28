from typing import List, Optional
from schemas.client import ClientCreate, ClientResponse
from infrastructure.uow import UnitOfWork
from domain.client import Client

async def create_client(client_data: ClientCreate, uow: UnitOfWork) -> ClientResponse:
    async with uow:
        new_client = Client(name=client_data.name, email=client_data.email, phone=client_data.phone)
        added_client = await uow.clients.add(new_client)
        await uow.commit()
        return ClientResponse(id=added_client.id, name=added_client.name, email=added_client.email, phone=added_client.phone)

async def get_client(client_id: int, uow: UnitOfWork) -> Optional[ClientResponse]:
    async with uow:
        client = await uow.clients.get(client_id)
        if client:
            return ClientResponse(id=client.id, name=client.name, email=client.email, phone=client.phone)
        return None

async def list_clients(uow: UnitOfWork) -> List[ClientResponse]:
    async with uow:
        clients = await uow.clients.list()
        return [ClientResponse(id=c.id, name=c.name, email=c.email, phone=c.phone) for c in clients]
