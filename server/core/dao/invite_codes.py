from fastapi.encoders import jsonable_encoder

from core.dao.database import db
from core.schemas.utils import InviteCode


async def add_invite_code(invite_code: InviteCode):
    return await db.invite_codes.insert_one(jsonable_encoder(invite_code))


async def get_invite_code(invite_code: str):
    obj = await db.invite_codes.find_one({"invite_code": invite_code})
    if obj is not None:
        return InviteCode(**obj)


async def invite_code_exists(invite_code: str):
    return await get_invite_code(invite_code) is not None
