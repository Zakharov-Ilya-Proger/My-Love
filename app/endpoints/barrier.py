from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.db.barrier_db import db_post_person_entrances
from app.models.barrier_model import AddEnterExit
from app.tokens.decode import decode_token
from app.tokens.descriptions import enter_token

barrier_router = APIRouter()


api_key_header = APIKeyHeader(name="Authorization")

@barrier_router.post("/add", description=enter_token)
async def enter_exit(enter_exit_data: AddEnterExit, authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None:
        raise HTTPException(status_code=403, detail="You no rights to enter or exit")
    funcs = {1: db_post_person_entrances("entryexithistory_admin", token, "admin_id", enter_exit_data),
             3: db_post_person_entrances("entryexithistory_student", token, "student_id", enter_exit_data),
             2: db_post_person_entrances("entryexithistory_teacher", token, "teacher_id", enter_exit_data),
             4: db_post_person_entrances("entryexithistory_staff", token, "staff_id", enter_exit_data)}
    raise await funcs[token['role_id']]
