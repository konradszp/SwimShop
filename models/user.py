from enum import Enum
from dataclasses import dataclass, field

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    SELLER = "SELLER"

@dataclass
class User:
    user_id: int | None
    username: str
    password_hash: str = field(repr=False)
    full_name: str
    role: UserRole