from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from schemas.client import ClientResponse
from schemas.task_file import TaskFileResponse
from schemas.audit_log import AuditLogResponse

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: Optional[str] = "sale"
    company_name: Optional[str] = None
    amount: Optional[float] = None
    client_id: Optional[int] = None

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
    comment: Optional[str] = None
    user_id: int
    is_deleted: bool
    client_id: Optional[int] = None
    
    client: Optional[ClientResponse] = None
    files: List[TaskFileResponse] = []
    audit_logs: List[AuditLogResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
