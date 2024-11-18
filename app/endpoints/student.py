from typing import Annotated
from fastapi import APIRouter, Header, HTTPException
from app.db.entryexit_db import db_get_person_entrances
from app.db.get_student import get_student_by_token_db
from app.db.lessons import get_lessons_from_db
from app.models.entry_exit import EnExHistory
from app.models.group import StudentInfo
from app.models.lesson import Lessons
from app.models.student import Student
from app.tokens.decode import decode_token

student = APIRouter()


@student.get("/entrances", response_model=EnExHistory)
async def get_entrances(access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    response = await db_get_person_entrances(
        token['id'],
        'student_id',
        'entryexithistory_student')
    return response


@student.get("/lessons", response_model=Lessons)
async def get_lessons(access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    response = await get_lessons_from_db(token['group'])
    return response


@student.get("/info", response_model=Student)
async def get_student_info(access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return await get_student_by_token_db(token['id'])

