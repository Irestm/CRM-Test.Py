from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    hashed_password: str
    id: Optional[int] = None
