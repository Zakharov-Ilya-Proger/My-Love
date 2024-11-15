from fastapi import APIRouter

from app.endpoints.N.lessons import lessons
from app.endpoints.N.login_refresh_reset import login_reset_refresh

neutral = APIRouter()

neutral.include_router(login_reset_refresh)
neutral.include_router(lessons)