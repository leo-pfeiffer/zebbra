import motor.motor_asyncio
from core.settings import get_settings

_settings = get_settings()


def get_db_url():
    user = _settings.dict()['MONGODB_USER']
    pw = _settings.dict()['MONGODB_PW']
    url = _settings.dict()['MONGODB_URL']
    db = _settings.dict()['MONGODB_DB']
    return f"mongodb://{user}:{pw}@{url}/{db}?retryWrites=true&w=majority"


client = motor.motor_asyncio.AsyncIOMotorClient(get_db_url())
db = client.zebbra
