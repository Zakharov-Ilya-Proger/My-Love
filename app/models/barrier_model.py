from datetime import datetime
from pydantic import BaseModel


class AddEnterExit(BaseModel):
    time: datetime
    status: str
    branch_id: int
