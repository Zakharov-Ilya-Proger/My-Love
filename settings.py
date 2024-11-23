import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Users Microservice"
    APP_PORT: int = os.getenv("APP_PORT")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)
    REFRESH_TOKEN_EXPIRED_HOURS: int = os.getenv("REFRESH_TOKEN_EXPIRE_HOURS", 1)

    class Config:
        env_file = ".env"


load_dotenv()

settings = Settings()
