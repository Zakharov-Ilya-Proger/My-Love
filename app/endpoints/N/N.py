from fastapi import APIRouter

from app.endpoints.N.lessons import lessons

neutral = APIRouter()

neutral.include_router(lessons, prefix="/lessons")