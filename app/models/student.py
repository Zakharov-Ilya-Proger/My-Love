from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str
    secondname: str
    lastname: str
    group: str
    institute: str
