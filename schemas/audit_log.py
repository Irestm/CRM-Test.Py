from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AuditLogBase(BaseModel):
    task_id: int
    user_id: int
    action: str
    description: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogResponse(AuditLogBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
