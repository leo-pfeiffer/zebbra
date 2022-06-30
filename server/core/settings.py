from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "prod"

    MAX_MODELS: int = 10000
    INVITE_CODE_EXPIRE: int

    AUTH_SECRET: str
    AUTH_ALGO: str
    AUTH_TOKEN_EXPIRE: int

    MONGODB_USER: str
    MONGODB_DB: str
    MONGODB_PW: str
    MONGODB_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()
