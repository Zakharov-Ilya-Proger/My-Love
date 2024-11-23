from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_headers=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],)

from app.endpoints.admin_login import admin_router
from app.endpoints.teacher_login import teacher_router
from app.endpoints.user_login import user_router

app.include_router(admin_router, prefix="/api/auth/admin", tags=["Admin"])
app.include_router(user_router, prefix="/api/auth/student", tags=["Student"])
app.include_router(teacher_router, prefix="/api/auth/teacher", tags=["Teacher"])
