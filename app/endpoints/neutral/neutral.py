from typing import Annotated

from fastapi import APIRouter, Header

from app.db.lessons import get_lesson_from_db
from app.models.lesson import Lesson
from app.tokens.decode import decode_token

neutral = APIRouter()


@neutral.get("/{lesson_id}", response_model=Lesson)
async def get_lesson(lesson_id: str, access_token: Annotated[str | None, Header()] = None):
    decode_token(access_token)
    response = await get_lesson_from_db(lesson_id)
    return response
