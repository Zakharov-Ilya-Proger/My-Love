from datetime import datetime
from typing import List

from pydantic import BaseModel


class EnEx(BaseModel):
    branch_name: str
    branch_address: str
    time: datetime
    status: str


class EnExHistory(BaseModel):
    history: List[EnEx]


class AddEnterExit(BaseModel):
    time: datetime
    status: str
    branch_id: str
