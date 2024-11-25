from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class LessonTeacher(BaseModel):
    id: int
    subject: str
    group: str
    auditory_name: str
    auditory_capacity: int
    branch_name: str
    branch_address: str
    start_time: datetime
    end_time: datetime
    task: Optional[str]
    deadline: Optional[datetime]
    type_of_lesson: str


class LessonsTeacher(BaseModel):
    lessons: List[LessonTeacher]
