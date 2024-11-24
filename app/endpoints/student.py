from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from app.db.get_data_for_per_and_gpa import get_data_for_gpa
from app.db.get_grade import grade_for_student
from app.db.get_student import get_student_by_token_db
from app.db.lessons import get_lessons_from_db
from app.models.Statist import GPA
from app.models.grade import StudentGrade
from app.models.lesson import Lessons
from app.models.student import Student
from app.tokens.decode import decode_token

student = APIRouter()

api_key_header = APIKeyHeader(name="Authorization")


@student.get("/lessons", response_model=Lessons)
async def get_lessons(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    response = await get_lessons_from_db(token['group'])
    if isinstance(response, Lessons):
        return response
    raise response


@student.get("/info", response_model=Student)
async def get_student_info(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    response = await get_student_by_token_db(token['id'])
    if isinstance(response, Student):
        return response
    raise response


@student.get("/gpa", response_model=GPA)
async def get_student_percentile(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    response = await get_data_for_gpa(token['id'])
    if isinstance(response, GPA):
        return {'gpa': response}
    raise response


@student.get("/grade", response_model=StudentGrade)
async def get_student_grade(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    response = await grade_for_student(token['id'])
    if isinstance(response, StudentGrade):
        return response
    raise response
