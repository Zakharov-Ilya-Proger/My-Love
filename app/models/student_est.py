from pydantic import BaseModel


class EstForStudent(BaseModel):
    student_id: int
    lesson_id: int
    mark: int
