from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from app.db.enter_token import get_enter_token
from app.db.entryexit_db import db_get_person_entrances
from app.db.lessons import get_lesson_from_lesson_id_db
from app.models.entry_exit import EnExHistory
from app.models.lesson import Lesson
from app.tokens.decode import decode_token

neutral = APIRouter()


api_key_header = APIKeyHeader(name="Authorization")

@neutral.get("/lesson/{lesson_id}", response_model=Lesson)
async def get_lesson(lesson_id: int, authorization: Annotated[str | None, Depends(api_key_header)] = None):
    decode_token(authorization)
    if authorization is None:
        raise HTTPException(status_code=403, detail="Authorization header missing")
    response = await get_lesson_from_lesson_id_db(lesson_id)
    if isinstance(response, Lesson):
        return response
    raise response


@neutral.get("/entrances", response_model=EnExHistory)
async def get_entrances(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    funcs = {"admin": db_get_person_entrances(token["id"],"admin_id","entryexithistory_admin"),
             "student": db_get_person_entrances(int(token['id']), "student_id", "entryexithistory_student"),
             "teacher": db_get_person_entrances(token['id'], "teacher_id", "entryexithistory_teacher"),
             "staff": db_get_person_entrances(token['id'], "staff_id", "entryexithistory_staff")}
    response = await funcs[token['role']]
    if isinstance(response, EnExHistory):
        return response
    raise response


@neutral.get("/enter/token")
async def get_enter_token_end(authorisation: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorisation)
    if token is None:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    funcs = {"admin": get_enter_token("admins", token["id"]),
             "student": get_enter_token("students", token["id"]),
             "teacher": get_enter_token("teachers", token["id"])
    }
    response = await funcs[token['role']]
    if isinstance(response, HTTPException):
        raise response
    return {"enter_token": response}
