from typing import Dict, List
from pydantic import BaseModel, Field, RootModel


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


class StudentGrades(BaseModel):
    FIO: str
    s_id: int
    marks: List[int]

class GroupGrades(RootModel):
    root: List[StudentGrades]

class SubjectGrades(RootModel):
    root: Dict[str, GroupGrades]

class TeacherGrade(RootModel):
    root: Dict[str, SubjectGrades]

