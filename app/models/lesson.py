from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Lesson(BaseModel):
    id: int
    subject: str
    group: str
    auditory_name: str
    auditory_capacity: int
    branch_name: str
    branch_address: str
    start_time: datetime
    end_time: datetime
    teacher_name: str
    teacher_secondname: str
    teacher_lastname: str
    task: Optional[str]
    deadline: Optional[datetime]
    type_of_lesson: str


class Lessons(BaseModel):
    lessons: List[Lesson]
