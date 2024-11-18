from fastapi import FastAPI

app = FastAPI()

from app.endpoints.main import main
from app.endpoints.student import student
from app.endpoints.teacher import teacher
from app.endpoints.neutral import neutral

app.include_router(main)
app.include_router(student, prefix="/student")
app.include_router(teacher, prefix="/teacher")
app.include_router(neutral, prefix="/neutral")
