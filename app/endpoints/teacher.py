from fastapi import APIRouter, Header, HTTPException
from typing import Annotated
from app.db.add_mark import add_mark_for_student
from app.db.add_marking import add_students_marking
from app.db.entryexit_db import db_get_person_entrances
from app.db.get_group import get_group_db
from app.db.get_student import get_student_db
from app.db.get_teacher_disciplines import teacher_disciplines
from app.db.groups import get_groups_db
from app.db.teacher_lessons import get_teacher_lessons
from app.models.disciplines_model import Disciplines
from app.models.entry_exit import EnExHistory
from app.models.group_info import GroupInfo
from app.models.student import Student
from app.models.student_est import EstForStudent
from app.models.students_on_lesson import StudentsOnLesson
from app.models.teacher_lessons import LessonsTeacher
from app.tokens.decode import decode_token

teacher = APIRouter()


@teacher.get("/groups", response_model=GroupInfo)
async def get_groups(access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to set estimations')
    return await get_groups_db(token['id'])


@teacher.post("/mark")
async def add_mark(mark: EstForStudent, access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to set estimations')
    await add_mark_for_student(mark)


@teacher.get("/student/{student_code}", response_model=Student)
async def get_student(student_code: str, access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to get this information')
    return await get_student_db(student_code)


@teacher.get("/lessons", response_model=LessonsTeacher)
async def teacher_lessons(access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to get this information')
    return await get_teacher_lessons(token['id'])


@teacher.post("/marking/students")
async def marking_students(students: StudentsOnLesson, access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to set this information')
    return await add_students_marking(students)


@teacher.get("/disciplines", response_model=Disciplines)
async def get_disciplines(access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to get this information')
    return await teacher_disciplines(token['id'])


@teacher.get("/group/{group_code}")
async def get_group(group_code: int, access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to get this information')
    return await get_group_db(group_code)


@teacher.get("/entrances", response_model=EnExHistory)
async def get_entrances(access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return await db_get_person_entrances(
        token['id'],
        'teacher_id',
        'entryexithistory_teacher')
