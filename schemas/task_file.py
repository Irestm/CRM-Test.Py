from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TaskFileBase(BaseModel):
    file_path: str
    file_name: str

class TaskFileCreate(TaskFileBase):
    task_id: int

class TaskFileResponse(TaskFileBase):
    id: int
    task_id: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
