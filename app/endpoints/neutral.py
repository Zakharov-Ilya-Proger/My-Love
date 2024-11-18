from typing import Annotated
from fastapi import APIRouter, Header, HTTPException

from app.db.entryexit_db import db_post_person_entrances
from app.db.lessons import get_lesson_from_db
from app.models.entry_exit import AddEnterExit
from app.models.lesson import Lesson
from app.tokens.decode import decode_token

neutral = APIRouter()


@neutral.get("/{lesson_id}", response_model=Lesson)
async def get_lesson(lesson_id: str, access_token: Annotated[str | None, Header()] = None):
    decode_token(access_token)
    response = await get_lesson_from_db(lesson_id)
    return response

@neutral.post("/enter/exit")
async def enter_exit(enter_exit_data: AddEnterExit, enter_token: Annotated[str | None, Header()] = None):
    token = decode_token(enter_token)
    if token is None:
        raise HTTPException(status_code=403, detail="You no rights to enter or exit")
    funcs = {'admin': db_post_person_entrances('entryexithistory_admin', token, enter_exit_data),
             'student': db_post_person_entrances('entryexithistory_student', token, enter_exit_data),
             'teacher': db_post_person_entrances('entryexithistory_teacher', token, enter_exit_data),
             'staff': db_post_person_entrances('entryexithistory_staff', token, enter_exit_data),}
    await funcs[token['role']]