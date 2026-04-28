from typing import Optional
from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: Optional[str] = "sale"
    company_name: Optional[str] = None
    amount: Optional[float] = None

class TaskUpdateStatus(BaseModel):
    status: str
    comment: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    task_type: str
    company_name: Optional[str] = None
    amount: Optional[float] = None
    file_path: Optional[str] = None
    comment: Optional[str] = None
    user_id: int
    is_deleted: bool
    
    model_config = ConfigDict(from_attributes=True)