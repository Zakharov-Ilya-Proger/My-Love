from typing import Dict, List
from pydantic import BaseModel, RootModel


class StudentGroupInfo(BaseModel):
    id: int
    name: str
    secondname: str
    lastname: str
    code: str


class GroupInfo(RootModel):
    root: Dict[str, List[StudentGroupInfo]]
