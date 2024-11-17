from typing import List, Dict

from pydantic import BaseModel


class StudentInfo(BaseModel):
    id: int
    name: str
    secondname: str
    lastname: str
    code: str


class Group(BaseModel):
    group_code: str
    group: Dict[str, List[StudentInfo]]