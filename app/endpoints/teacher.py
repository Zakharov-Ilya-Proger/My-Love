from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from fastapi.security import APIKeyHeader
from app.db.add_mark import add_mark_for_student
from app.db.add_marking import add_students_marking
from app.db.get_grade import get_students_grade_for_teacher
from app.db.get_group import get_group_db
from app.db.get_student import get_student_db
from app.db.get_teacher_disciplines import teacher_disciplines
from app.db.groups import get_groups_db
from app.db.teacher_lessons import get_teacher_lessons
from app.models.disciplines_model import Disciplines
from app.models.grade import TeacherGrade
from app.models.group import Group
from app.models.group_info import GroupInfo
from app.models.student import Student
from app.models.student_est import EstForStudent
from app.models.students_on_lesson import StudentsOnLesson
from app.models.teacher_lessons import LessonsTeacher
from app.tokens.decode import decode_token

teacher = APIRouter()

api_key_header = APIKeyHeader(name="Authorization")


@teacher.get("/groups", response_model=GroupInfo)
async def get_groups(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to set estimations')
    response = await get_groups_db(token['id'])
    if isinstance(response, GroupInfo):
        return response
    raise response


@teacher.post("/mark")
async def add_mark(mark: EstForStudent, authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to set estimations')
    raise await add_mark_for_student(mark)


@teacher.get("/student/{student_code}", response_model=Student)
async def get_student(student_code: str, authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to get this information')
    response = await get_student_db(student_code)
    if isinstance(response, Student):
        return response
    raise response


@teacher.get("/lessons", response_model=LessonsTeacher)
async def teacher_lessons(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to get this information')
    response = await get_teacher_lessons(token['id'])
    if isinstance(response, LessonsTeacher):
        return response
    raise response


@teacher.post("/marking/students")
async def marking_students(students: StudentsOnLesson,
                           authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to set this information')
    raise await add_students_marking(students)


@teacher.get("/disciplines", response_model=Disciplines)
async def get_disciplines(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to get this information')
    response = await teacher_disciplines(token['id'])
    if isinstance(response, Disciplines):
        return response
    raise response


@teacher.get("/group/{group_code}", response_model=Group)
async def get_group(group_code: int, authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to get this information')
    response = await get_group_db(group_code)
    if isinstance(response, Group):
        return response
    raise response


@teacher.get("/all/grades", response_model=TeacherGrade)
async def get_students_grade(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token['role'] != 'teacher' or token is None:
        raise HTTPException(status_code=403, detail='You have no rights to get this information')
    response = await get_students_grade_for_teacher(token['id'])
    if isinstance(response, TeacherGrade):
        return response
    raise response