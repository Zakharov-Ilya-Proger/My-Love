from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_headers=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],)

from app.endpoints.main import main
from app.endpoints.student import student
from app.endpoints.teacher import teacher
from app.endpoints.neutral import neutral

app.include_router(main, prefix="api/users" ,tags=["Main"])
app.include_router(student, prefix="api/users/student", tags=["Student"])
app.include_router(teacher, prefix="api/users/teacher", tags=["Teacher"])
app.include_router(neutral, prefix="api/users/neutral", tags=["Neutral"])
