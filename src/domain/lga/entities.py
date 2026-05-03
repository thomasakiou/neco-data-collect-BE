from dataclasses import dataclass
from typing import Optional

@dataclass
class LGA:
    state_name: str
    state_code: str
    lga_name: str
    lga_code: str
    id: Optional[int] = None
