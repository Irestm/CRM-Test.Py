from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    title: str
    user_id: int
    description: Optional[str] = None
    status: str = "new"
    file_path: Optional[str] = None
    comment: Optional[str] = None
    is_deleted: bool = False
    id: Optional[int] = None