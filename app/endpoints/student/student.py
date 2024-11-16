from typing import Annotated

from fastapi import APIRouter, Header

from app.db.entryexit_db import db_get_student_entrances
from app.tokens.generate import decode_token

student = APIRouter()


@student.get("/entrances")
async def get_entrances(access_token: Annotated[str | None, Header()] = None):
    student_id = decode_token(access_token)['id']
    response = await db_get_student_entrances(student_id)
    return response
