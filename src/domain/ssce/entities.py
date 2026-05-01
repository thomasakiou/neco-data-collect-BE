from dataclasses import dataclass
from typing import Optional

@dataclass
class SSCE:
    state_code: str
    state_name: str
    sch_num: str
    sch_name: str
    cust_code: str
    cust_name: str
    cust_town: str
    status: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    accd_year: Optional[str] = None
    lga: Optional[str] = None
    id: Optional[int] = None
