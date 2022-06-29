from typing import Any

from fastapi.encoders import jsonable_encoder

from core.exceptions import UniqueConstraintFailedException, BusinessLogicException
from core.dao.database import db
from core.objects import PyObjectId
from core.schemas.users import UserInDB, RegisterUser


async def user_exists(user_id: PyObjectId):
    return await get_user(user_id) is not None


async def username_exists(username: str):
    return await get_user_by_username(username) is not None


async def get_user(user_id: PyObjectId) -> UserInDB | None:
    user = await db.users.find_one({"_id": str(user_id)})
    if user is not None:
        return UserInDB(**user)


async def get_user_by_username(username: str) -> UserInDB | None:
    user = await db.users.find_one({"username": username})
    if user is not None:
        return UserInDB(**user)


async def get_user_id(username: str) -> str:
    user = await db.users.find_one({"username": username})
    if user is not None:
        return user.id


async def get_username(user_id: PyObjectId) -> str:
    user = await db.users.find_one({"_id": str(user_id)})
    if user is not None:
        return user.username


async def create_user(user: UserInDB):
    if await username_exists(user.username):
        raise UniqueConstraintFailedException("Username must be unique")
    return await db.users.insert_one(jsonable_encoder(user))


async def update_username(user_id: PyObjectId, new_username: str):
    if await username_exists(new_username):
        raise UniqueConstraintFailedException("Username must be unique")

    await db.users.update_one(
        {"_id": str(user_id)},
        {"$set": {"username": new_username}},
    )


async def update_user_field(user_id: PyObjectId, field: str, value: Any):
    assert field != "username"
    if field not in RegisterUser.__fields__ and field != "hashed_password":
        raise ValueError(f"Setting {field} not supported.")
    await db.users.update_one({"_id": str(user_id)}, {"$set": {field: value}})
    return await db.users.find_one({"_id": str(user_id)})


async def delete_user_full(user_id: PyObjectId):
    """
    Fully delete a user including and remove from all workspaces etc.
    :param user_id: username of user to delete
    """
    # remove user object itself
    await db.users.delete_one({"_id": str(user_id)})

    # remove user from workspaces
    await db.workspaces.update_many(
        {"users": str(user_id)}, {"$pull": {"users": str(user_id)}}
    )

    # remove from models
    await db.models.update_many(
        {
            "$or": [
                {"meta.admins": str(user_id)},
                {"meta.editors": str(user_id)},
                {"meta.viewers": str(user_id)},
            ]
        },
        {
            "$pull": {
                "meta.admins": str(user_id),
                "meta.editors": str(user_id),
                "meta.viewers": str(user_id),
            },
        },
    )


async def remove_user_from_workspace(user_id: PyObjectId, workspace_id: PyObjectId):

    # cannot remove admin from workspace
    if (
        await db.workspaces.count_documents(
            {"admin": str(user_id), "_id": str(workspace_id)}
        )
        > 0
    ):
        raise BusinessLogicException("Cannot remove admin from workspace.")

    # cannot remove user if they are sole admin of model
    if (
        await db.models.count_documents(
            {"meta.admins": str(user_id), "meta.admins.1": {"$exists": False}}
        )
        > 0
    ):
        raise BusinessLogicException("Cannot remove sole admin from model.")

    # remove user from workspace
    await db.workspaces.update_one(
        {"_id": str(workspace_id)}, {"$pull": {"users": str(user_id)}}
    )

    # remove user from all models of workspace
    await db.models.update_many(
        {"meta.workspace": str(workspace_id)},
        {
            "$pull": {
                "meta.admins": str(user_id),
                "meta.editors": str(user_id),
                "meta.viewers": str(user_id),
            },
        },
    )


async def add_user_to_workspace(user_id: PyObjectId, workspace_id: PyObjectId):
    # add user to workspace
    await db.workspaces.update_one(
        {"_id": str(workspace_id)}, {"$push": {"users": str(user_id)}}
    )


async def set_user_otp_secret(user_id: PyObjectId, otp_secret: str):
    await db.users.update_one(
        {"_id": str(user_id)},
        {"$set": {"otp_secret": otp_secret, "otp_validated": False}},
    )


async def set_user_otp_secret_validated(user_id: PyObjectId):
    await db.users.update_one(
        {"_id": str(user_id)},
        {"$set": {"otp_validated": True}},
    )
