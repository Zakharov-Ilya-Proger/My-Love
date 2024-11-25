from typing import List, Optional
from pydantic import BaseModel


class Teacher(BaseModel):
    name: str
    secondname: str
    lastname: str
    code: str
    dep_name: str
    institute: str
    subjects: Optional[List[str]]
