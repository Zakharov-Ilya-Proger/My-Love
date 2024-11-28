from typing import List, Dict
from pydantic import BaseModel, RootModel


class StudentInfo(BaseModel):
    id: int
    name: str
    secondname: str
    lastname: str
    code: str


class Group(RootModel):
    root: List[StudentInfo]