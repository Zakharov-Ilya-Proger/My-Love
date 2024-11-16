from fastapi import FastAPI

from app.login import login_endpoint
from main import main_router

app = FastAPI()

app.include_router(main_router)
app.include_router(login_endpoint)
