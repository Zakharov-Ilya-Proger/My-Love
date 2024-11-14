from fastapi import FastAPI


app = FastAPI()

from .main import main_router
from teacher.teacher import teacher
from student.student import student
from app.login.login_register_refresh import login_reset_refresh

app.include_router(main_router)
app.include_router(student, prefix="/student")
app.include_router(teacher, prefix="/teacher")
app.include_router(login_reset_refresh)
