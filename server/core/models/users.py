from fastapi.encoders import jsonable_encoder

from core.models.database import db
from core.schemas.users import UserInDB


async def get_user(username: str):
    user = await db["users"].find_one({"username": username})
    if user is not None:
        return UserInDB(**user)


async def create_user(user: UserInDB):
    res = await db["users"].insert_one(jsonable_encoder(user))
    return res
