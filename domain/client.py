from dataclasses import dataclass
from typing import Optional

@dataclass
class Client:
    name: str
    email: str
    phone: str
    id: Optional[int] = None
