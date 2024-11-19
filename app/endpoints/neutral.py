from typing import Annotated
from fastapi import APIRouter, Header, HTTPException
from app.db.entryexit_db import db_post_person_entrances, db_get_person_entrances
from app.db.lessons import get_lesson_from_db
from app.models.entry_exit import AddEnterExit, EnExHistory
from app.models.lesson import Lesson
from app.tokens.decode import decode_token
from app.tokens.descriptions import enter_token, access_token

neutral = APIRouter()


@neutral.get("/{lesson_id}", response_model=Lesson, description=access_token)
async def get_lesson(lesson_id: str, authorization: Annotated[str | None, Header()] = None):
    decode_token(authorization)
    response = await get_lesson_from_db(lesson_id)
    return response


@neutral.post("/enter/exit", description=enter_token)
async def enter_exit(enter_exit_data: AddEnterExit, authorization: Annotated[str | None, Header()] = None):
    token = decode_token(authorization)
    if token is None:
        raise HTTPException(status_code=403, detail="You no rights to enter or exit")
    funcs = {'admin': db_post_person_entrances('entryexithistory_admin', token, enter_exit_data),
             'student': db_post_person_entrances('entryexithistory_student', token, enter_exit_data),
             'teacher': db_post_person_entrances('entryexithistory_teacher', token, enter_exit_data),
             'staff': db_post_person_entrances('entryexithistory_staff', token, enter_exit_data)}
    await funcs[token['role']]


@neutral.get("/entrances", response_model=EnExHistory, description=access_token)
async def get_entrances(authorization: Annotated[str | None, Header()] = None):
    token = decode_token(authorization)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    funcs = {'admin': db_get_person_entrances(token['id'],'teacher_id','entryexithistory_teacher'),
             'student': db_get_person_entrances(token['id'], 'admin_id', 'entryexithistory_admin'),
             'teacher': db_get_person_entrances(token['id'], 'student_id', 'entryexithistory_student'),
             'staff': db_get_person_entrances(token['id'], 'staff_id', 'entryexithistory_staff')}
    return await funcs[token['role']]
