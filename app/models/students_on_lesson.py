from typing import Dict

from pydantic import BaseModel


class StudentsOnLesson(BaseModel):
    lesson_id: int
    students: Dict[int, bool]
