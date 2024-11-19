from fastapi import FastAPI

app = FastAPI()

from app.endpoints.main import main
from app.endpoints.student import student
from app.endpoints.teacher import teacher
from app.endpoints.neutral import neutral

app.include_router(main)
app.include_router(student, prefix="/student", tags=["student"])
app.include_router(teacher, prefix="/teacher", tags=["teacher"])
app.include_router(neutral, prefix="/neutral", tags=["neutral"])
