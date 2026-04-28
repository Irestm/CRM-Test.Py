from pydantic import BaseModel, EmailStr, ConfigDict

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

class ClientResponse(ClientCreate):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
