from pydantic import BaseModel


class Percentile(BaseModel):
    percentile: float


class GPA(BaseModel):
    gpa: float