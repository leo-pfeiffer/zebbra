from fastapi.encoders import jsonable_encoder

from core.exceptions import UniqueConstraintFailedException
from core.dao.database import db
from core.schemas.users import UserInDB


async def get_user(username: str):
    user = await db.users.find_one({"username": username})
    if user is not None:
        return UserInDB(**user)


async def create_user(user: UserInDB):
    if await get_user(user.username) is not None:
        raise UniqueConstraintFailedException("Username must be unique")
    res = await db.users.insert_one(jsonable_encoder(user))
    return res


async def delete_user_full(username: str):
    """
    Fully delete a user including and remove from all workspaces etc.
    :param username: username of user to delete
    """
    # remove user object itself
    await db.users.delete_one({"username": username})

    # remove user from workspaces
    await db.workspaces.update_many({"users": username}, {"$pull": {"users": username}})


async def add_user_to_workspace(username: str, workspace: str):
    # add workspace to user
    await db.users.update_one(
        {"username": username}, {"$push": {"workspaces": workspace}}
    )

    # add user to workspace
    await db.workspaces.update_one({"name": workspace}, {"$push": {"users": username}})