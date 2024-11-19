from fastapi import FastAPI

app = FastAPI()

from app.endpoints.admin_login import admin_router
from app.endpoints.main import main_router
from app.endpoints.teacher_login import teacher_router
from app.endpoints.user_login import user_router


app.include_router(main_router)
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(teacher_router, prefix="/teacher", tags=["teacher"])
