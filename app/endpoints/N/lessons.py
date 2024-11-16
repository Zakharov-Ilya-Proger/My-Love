from typing import Annotated

from fastapi import APIRouter, Header

from app.db.lessons import get_lessons_from_db, get_lesson_from_db
from app.models.lesson import Lessons, Lesson
from app.tokens.generate import decode_token

lessons = APIRouter()


@lessons.get("/", response_model=Lessons)
async def get_lessons(access_token: Annotated[str | None, Header()] = None):
    group = decode_token(access_token)['group']
    response = await get_lessons_from_db(group)
    return response


@lessons.get("/{lesson_id}", response_model=Lesson)
async def get_lesson(lesson_id: str, access_token: Annotated[str | None, Header()] = None):
    group = decode_token(access_token)
    response = await get_lesson_from_db(lesson_id)
    return response
