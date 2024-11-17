from typing import Annotated

from fastapi import APIRouter, Header

from app.db.entryexit_db import db_get_student_entrances
from app.db.lessons import get_lessons_from_db
from app.models.lesson import Lessons
from app.tokens.decode import decode_token

student = APIRouter()


@student.get("/entrances")
async def get_entrances(access_token: Annotated[str | None, Header()] = None):
    student_id = decode_token(access_token)['id']
    response = await db_get_student_entrances(student_id)
    return response


@student.get("/lessons", response_model=Lessons)
async def get_lessons(access_token: Annotated[str | None, Header()] = None):
    group = decode_token(access_token)['group']
    response = await get_lessons_from_db(group)
    return response
