from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_USER: str
    MONGODB_DB: str
    MONGODB_PW: str
    MONGODB_URL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings()
