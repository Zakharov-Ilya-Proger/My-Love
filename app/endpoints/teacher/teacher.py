from fastapi import APIRouter, Header, HTTPException
from typing import Annotated

from app.db.add_mark import add_mark_for_student
from app.db.groups import get_groups_db
from app.models.group_info import GroupInfo
from app.models.student_est import EstForStudent
from app.tokens.generate import decode_token

teacher = APIRouter()


@teacher.get("/groups", response_model=GroupInfo)
async def get_groups(access_token: Annotated[str | None, Header()] = None):
    teacher_id = decode_token(access_token)['id']
    response = await get_groups_db(teacher_id)
    return response


@teacher.post("/estimation")
async def add_estimation(mark: EstForStudent, access_token: Annotated[str | None, Header()] = None):
    token = decode_token(access_token)
    if token['role'] != 'teacher':
        raise HTTPException(status_code=403, detail='You have no rights to set estimations')
    await add_mark_for_student(mark)
