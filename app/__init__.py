from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.endpoints.auditories import auditory_router
from app.endpoints.barrier import barrier_router

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_headers=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],)


app.include_router(barrier_router, prefix="/api/entrance")
app.include_router(auditory_router, prefix="/api/entrance")
