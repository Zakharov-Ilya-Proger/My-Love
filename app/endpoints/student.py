from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from app.db.get_data_for_per_and_gpa import get_data_for_gpa
from app.db.get_student import get_student_by_token_db
from app.db.lessons import get_lessons_from_db
from app.models.entry_exit import EnExHistory
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
    return await get_lessons_from_db(token['group'])


@student.get("/info", response_model=Student)
async def get_student_info(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return await get_student_by_token_db(token['id'])


@student.get("/gpa", response_model=EnExHistory)
async def get_student_percentile(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None or token['role'] != 'student':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    data, error = await get_data_for_gpa(token['id'])
    if error is None:
        raise HTTPException(status_code=404, detail="No data for this person")
    elif error is False:
        raise HTTPException(status_code=500, detail=f"DB error {data}")
    else:
        return {'gpa': data}
