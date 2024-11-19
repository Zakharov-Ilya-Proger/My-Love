from fastapi import FastAPI

from .admin.admin_login import admin_router
from .main import main_router
from .teacher.teacher_login import teacher_router
from .user.user_login import user_router

app = FastAPI()

app.include_router(main_router)
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(teacher_router, prefix="/teacher", tags=["teacher"])
