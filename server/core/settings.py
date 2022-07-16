from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "prod"

    MAX_MODELS: int = 10000
    INVITE_CODE_EXPIRE: int = 10080

    AUTH_SECRET: str
    AUTH_ALGO: str
    AUTH_TOKEN_EXPIRE: int

    MONGODB_USER: str
    MONGODB_DB: str
    MONGODB_PW: str
    MONGODB_URL: str

    XERO_CLIENT_ID: str
    XERO_CLIENT_SECRET: str
    XERO_CONF_URL: str = (
        "https://login.xero.com/identity/.well-known/openid-configuration"
    )
    XERO_API_BASE_URL: str = "https://api.xero.com/"
    XERO_API_URL_SUFFIX: str = "api.xro/2.0/"
    XERO_REFRESH_URL: str = "https://identity.xero.com/connect/token"

    GUSTO_CLIENT_ID: str
    GUSTO_CLIENT_SECRET: str
    GUSTO_CONF_URL: str = "https://api.gusto-demo.com/.well-known/openid-configuration"
    GUSTO_API_BASE_URL: str = "https://api.gusto-demo.com/"
    GUSTO_REFRESH_URL: str = "https://api.gusto-demo.com/oauth/token"
    GUSTO_AUTHORIZE_URL: str = "https://api.gusto-demo.com/oauth/authorize"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()
