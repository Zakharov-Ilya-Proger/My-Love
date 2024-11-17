from fastapi import FastAPI

app = FastAPI()

from .main import main_router
from app.endpoints.student.student import student
from app.endpoints.teacher.teacher import teacher
from app.endpoints.neutral.neutral import neutral

app.include_router(main_router)
app.include_router(student, prefix="/student")
app.include_router(teacher, prefix="/teacher")
app.include_router(neutral, prefix="/neutral")
