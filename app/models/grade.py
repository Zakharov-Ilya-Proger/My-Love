from typing import Dict, List

from pydantic import BaseModel, Field


class StudentGrade(BaseModel):
    subjects: Dict[str, List[int]] = Field(
        ...,
        description="Dict of subjects in the key and List of marks in value",
        examples=[{
            "Математика": [5, 4, 5],
            "Физика": [2, 2, 2],
            "Английский": [3, 4, 5, 5]
        }]
    )


class StudentGradesInGroup(BaseModel):
    FIO: str
    marks: int
    subjects: str


class TeacherGrade(BaseModel):
    groups: Dict[str, List[StudentGradesInGroup]] = Field()
