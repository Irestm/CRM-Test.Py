from typing import Optional
from pydantic import BaseModel, ConfigDict

class ClientBase(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    position: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
