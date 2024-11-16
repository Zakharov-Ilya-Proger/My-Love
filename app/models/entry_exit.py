from datetime import datetime
from typing import List

from pydantic import BaseModel


class EnEx(BaseModel):
    branch_name: str
    branch_address: str
    entry_time: datetime
    exit_time: datetime
    status: str


class EnExHistory(BaseModel):
    history: List[EnEx]
