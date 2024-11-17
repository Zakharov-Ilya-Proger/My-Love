from datetime import datetime

from pydantic import BaseModel

class StudentsOnLesson(BaseModel):
    lesson_id: int
    students_id: list
    check_in_time: datetime
    check_out_time: datetime
    status: str