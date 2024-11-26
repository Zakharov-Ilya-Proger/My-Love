from datetime import datetime
from pydantic import BaseModel


class AccessControl(BaseModel):
    audit_id: int
    time: datetime
    reason: str


class CloseAccess(BaseModel):
    audit_id: int
    time: datetime
