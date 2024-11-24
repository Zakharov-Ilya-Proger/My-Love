from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from app.db.enter_token import get_enter_token
from app.db.entryexit_db import db_post_person_entrances, db_get_person_entrances
from app.db.get_data_for_per_and_gpa import count_percentile_from_db
from app.db.lessons import get_lesson_from_lesson_id_db
from app.models.Statist import Percentile
from app.models.entry_exit import AddEnterExit, EnExHistory
from app.models.lesson import Lesson
from app.tokens.decode import decode_token
from app.tokens.descriptions import enter_token

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


@neutral.post("/enter/exit", description=enter_token)
async def enter_exit(enter_exit_data: AddEnterExit, authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None:
        raise HTTPException(status_code=403, detail="You no rights to enter or exit")
    funcs = {1: await db_post_person_entrances("entryexithistory_admin", token, "admin_id", enter_exit_data),
             3: await db_post_person_entrances("entryexithistory_student", token, "student_id", enter_exit_data),
             2: await db_post_person_entrances("entryexithistory_teacher", token, "teacher_id", enter_exit_data),
             4: await db_post_person_entrances("entryexithistory_staff", token, "staff_id", enter_exit_data)}
    raise funcs[token['role_id']]


@neutral.get("/entrances", response_model=EnExHistory)
async def get_entrances(authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    funcs = {"admin": await db_get_person_entrances(token["id"],"admin_id","entryexithistory_admin"),
             "student": await db_get_person_entrances(int(token['id']), "student_id", "entryexithistory_student"),
             "teacher": await db_get_person_entrances(token['id'], "teacher_id", "entryexithistory_teacher"),
             "staff": await db_get_person_entrances(token['id'], "staff_id", "entryexithistory_staff")}
    response = funcs[token['role']]
    if isinstance(response, EnExHistory):
        return response
    raise response


@neutral.get("/percentile", response_model=Percentile)
async def get_gpa(authorisation: Annotated[str | None, Depends(api_key_header)] = None,):
    token = decode_token(authorisation)
    if token is None or token['role'] not in ['student', 'teacher', 'admin']:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    response = await count_percentile_from_db()
    if isinstance(response, Percentile):
        return {"percentile":response}
    raise response


@neutral.get("/enter/token")
async def get_enter_token_end(authorisation: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorisation)
    if token is None:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    funcs = {"admin": await get_enter_token("admins", token["id"]),
             "student": await get_enter_token("students", token["id"]),
             "teacher": await get_enter_token("teachers", token["id"])
    }
    response = funcs[token['role']]
    if isinstance(response, HTTPException):
        raise response
    return {"enter_token": response}
