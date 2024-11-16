from fastapi import FastAPI

from app.login import login_endpoint

app = FastAPI()

app.include_router(login_endpoint)
