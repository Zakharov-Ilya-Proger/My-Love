from typing import Dict, List

from pydantic import BaseModel, Field


class StudentGroupInfo(BaseModel):
    id: int
    name: str
    secondname: str
    lastname: str
    code: str


class GroupInfo(BaseModel):
    groups: Dict[str, List[StudentGroupInfo]]