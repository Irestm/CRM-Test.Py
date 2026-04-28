from typing import Protocol, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.client import Client as ClientDomain
from infrastructure.orm import ClientModel

class ClientRepository(Protocol):
    async def add(self, client: ClientDomain) -> ClientDomain:
        ...
        
    async def get(self, client_id: int) -> Optional[ClientDomain]:
        ...
        
    async def list(self) -> List[ClientDomain]:
        ...

class SqlAlchemyClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, client: ClientDomain) -> ClientDomain:
        db_client = ClientModel(name=client.name, email=client.email, phone=client.phone)
        self.session.add(db_client)
        await self.session.flush()
        client.id = db_client.id
        return client

    async def get(self, client_id: int) -> Optional[ClientDomain]:
        stmt = select(ClientModel).where(ClientModel.id == client_id)
        result = await self.session.execute(stmt)
        db_client = result.scalar_one_or_none()
        if db_client:
            return ClientDomain(id=db_client.id, name=db_client.name, email=db_client.email, phone=db_client.phone)
        return None

    async def list(self) -> List[ClientDomain]:
        stmt = select(ClientModel)
        result = await self.session.execute(stmt)
        return [ClientDomain(id=c.id, name=c.name, email=c.email, phone=c.phone) for c in result.scalars()]
