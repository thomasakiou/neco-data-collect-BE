from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    state_code: str
    state_name: str
    hashed_password: str
    id: Optional[int] = None

    def verify_password(self, password: str) -> bool:
        # Business logic for password verification can go here 
        # (though implementation usually uses a service)
        pass
