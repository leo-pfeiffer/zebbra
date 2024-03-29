from fastapi.encoders import jsonable_encoder

from core.dao.database import db
from core.schemas.tokens import BlacklistToken


async def add_to_blacklist(token: BlacklistToken):
    return await db.token_blacklist.insert_one(jsonable_encoder(token))


async def get_blacklisted(access_token: str):
    return await db.token_blacklist.find_one({"access_token": access_token})


async def count_blacklisted_tokens():
    return await db.token_blacklist.count_documents({})


async def is_token_blacklisted(access_token: str):
    return await get_blacklisted(access_token) is not None
