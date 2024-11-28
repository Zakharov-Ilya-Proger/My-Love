from datetime import datetime
from typing import List
from pydantic import BaseModel, RootModel


class EnEx(BaseModel):
    branch_name: str
    branch_address: str
    time: datetime
    status: str


class EnExHistory(RootModel):
    root: List[EnEx]
