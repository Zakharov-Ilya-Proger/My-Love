from typing import List
import timestamp
from pydantic import BaseModel

class Lesson(BaseModel):
    id: int
    subject: str
    group: str
    auditory_name: str
    auditory_capacity: int
    branch_name: str
    branch_address: str
    start_time: timestamp
    end_time: timestamp
    teacher_name: str
    teacher_secondname: str
    teacher_lastname: str
    task: str
    deadline: timestamp

class Lessons(BaseModel):
    lessons: List[Lesson]