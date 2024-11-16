from fastapi import APIRouter
from app.admin.admin_login import admin_router
from app.teacher.teacher_login import teacher_router
from app.user.user_login import user_router

login_endpoint = APIRouter()

login_endpoint.include_router(admin_router, prefix="/admin")
login_endpoint.include_router(user_router, prefix="/user")
login_endpoint.include_router(teacher_router, prefix="/teacher")
