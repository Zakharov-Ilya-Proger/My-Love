from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.db.check_access import check_access_to_auditory_db
from app.db.close_access import close_access_to_auditory_db
from app.models.access_control import AccessControl, CloseAccess
from app.tokens.decode import decode_token

auditory_router = APIRouter()

api_key_header = APIKeyHeader(name="Authorization")


@auditory_router.post("/auditory/open")
async def check_access_to_auditory(access : AccessControl, authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token= decode_token(authorization)
    if token is None or token['role_id'] == 3:
        raise HTTPException(status_code=403, detail="Forbidden")
    funcs = {
        1: check_access_to_auditory_db("admin", "admin_id", access, token['id']),
        2: check_access_to_auditory_db("teacher", "teacher_id", access, token['id']),
        4: check_access_to_auditory_db("staff", "staff_id", access, token['id'])
    }
    raise await funcs[token['role_id']]


@auditory_router.put("/auditory/close")
async def close_auditory(access: CloseAccess, authorization: Annotated[str | None, Depends(api_key_header)] = None):
    token = decode_token(authorization)
    if token is None or token['role_id'] == 3:
        raise HTTPException(status_code=403, detail="Forbidden")
    funcs = {
        1: close_access_to_auditory_db("admin", "admin_id", access, token['id']),
        2: close_access_to_auditory_db("teacher", "teacher_id", access, token['id']),
        4: close_access_to_auditory_db("staff", "staff_id", access, token['id'])
    }
    raise await funcs[token['role_id']]
