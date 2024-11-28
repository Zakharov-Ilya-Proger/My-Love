from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, RootModel


class CustomLesson(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    auditory_id: Optional[int]


class CustomLessonForStudent(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    auditory: Optional[str]
    address: Optional[str]


class CustomLessons(RootModel):
    root: List[CustomLessonForStudent]
