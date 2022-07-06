import asyncio

import motor.motor_asyncio
from core.settings import get_settings

_settings = get_settings()


def get_db_url():
    user = _settings.dict()["MONGODB_USER"]
    pw = _settings.dict()["MONGODB_PW"]
    url = _settings.dict()["MONGODB_URL"]
    database = _settings.dict()["MONGODB_DB"]
    return f"mongodb://{user}:{pw}@{url}/{database}?retryWrites=true&w=majority"


class _DAO:
    _client = motor.motor_asyncio.AsyncIOMotorClient(get_db_url())
    _client.get_io_loop = asyncio.get_running_loop
    _db = _client[_settings.dict()["MONGODB_DB"]]

    users = _db["users"]
    workspaces = _db["workspaces"]
    token_blacklist = _db["token_blacklist"]
    invite_codes = _db["invite_codes"]
    models = _db["models"]
    integration_access = _db["integration_access"]

    @staticmethod
    def get_collection(collection):
        return getattr(_DAO, collection)

    @staticmethod
    def get_db():
        return _DAO._db


db = _DAO()
