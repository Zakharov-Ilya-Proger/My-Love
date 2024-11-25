from sys import prefix

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_headers=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],)

@app.get("/")
async def root():
    return {"Hello": "World"}