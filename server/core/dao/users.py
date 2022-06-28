from typing import Any

from fastapi.encoders import jsonable_encoder

from core.exceptions import UniqueConstraintFailedException, BusinessLogicException
from core.dao.database import db
from core.schemas.users import UserInDB, RegisterUser


async def user_exists(username: str):
    return await get_user(username) is not None


async def get_user(username: str) -> UserInDB | None:
    user = await db.users.find_one({"username": username})
    if user is not None:
        return UserInDB(**user)


async def create_user(user: UserInDB):
    if await get_user(user.username) is not None:
        raise UniqueConstraintFailedException("Username must be unique")
    res = await db.users.insert_one(jsonable_encoder(user))
    return res


async def update_username(username: str, new_username: str):
    if await get_user(new_username) is not None:
        raise UniqueConstraintFailedException("Username must be unique")

    await db.users.update_one(
        {"username": username},
        {"$set": {"username": new_username}},
    )

    # workspace admin
    await db.workspaces.update_many(
        {"admin": username}, {"$set": {"admin": new_username}}
    )

    # workspace users
    await db.workspaces.update_many(
        {"users": username},
        {"$push": {"users": new_username}},
    )
    await db.workspaces.update_many(
        {"users": username},
        {"$pull": {"users": username}},
    )

    # model admin
    await db.models.update_many(
        {"meta.admins": username},
        {"$push": {"meta.admins": new_username}},
    )
    await db.models.update_many(
        {"meta.admins": username},
        {"$pull": {"meta.admins": username}},
    )

    # model editor
    await db.models.update_many(
        {"meta.editors": username},
        {"$push": {"meta.editors": new_username}},
    )
    await db.models.update_many(
        {"meta.editors": username},
        {"$pull": {"meta.editors": username}},
    )

    # model viewer
    await db.models.update_many(
        {"meta.viewers": username},
        {"$push": {"meta.viewers": new_username}},
    )
    await db.models.update_many(
        {"meta.viewers": username},
        {"$pull": {"meta.viewers": username}},
    )


async def update_user_field(username: str, field: str, value: Any):
    assert field != "username"
    if field not in RegisterUser.__fields__ and field != "hashed_password":
        raise ValueError(f"Setting {field} not supported.")
    await db.users.update_one({"username": username}, {"$set": {field: value}})
    return await db.users.find_one({"username": username})


async def delete_user_full(username: str):
    """
    Fully delete a user including and remove from all workspaces etc.
    :param username: username of user to delete
    """
    # remove user object itself
    await db.users.delete_one({"username": username})

    # remove user from workspaces
    await db.workspaces.update_many({"users": username}, {"$pull": {"users": username}})


async def remove_user_from_workspace(username: str, workspace: str):

    # cannot remove admin from workspace
    if await db.workspaces.count_documents({"admin": username, "name": workspace}) > 0:
        raise BusinessLogicException("Cannot remove admin from workspace.")

    # cannot remove user if they are sole admin of model
    if (
        await db.models.count_documents(
            {"meta.admins": username, "meta.admins.1": {"$exists": False}}
        )
        > 0
    ):
        raise BusinessLogicException("Cannot remove sole admin from model.")

    await db.users.update_one(
        {"username": username}, {"$pull": {"workspaces": workspace}}
    )

    # remove user from workspace
    await db.workspaces.update_one({"name": workspace}, {"$pull": {"users": username}})

    # remove user from all models of workspace
    await db.models.update_many(
        {"meta.workspace": workspace},
        {
            "$pull": {
                "meta.admins": username,
                "meta.editors": username,
                "meta.viewers": username,
            },
        },
    )


async def add_user_to_workspace(username: str, workspace: str):
    # add workspace to user
    await db.users.update_one(
        {"username": username}, {"$push": {"workspaces": workspace}}
    )

    # add user to workspace
    await db.workspaces.update_one({"name": workspace}, {"$push": {"users": username}})


async def set_user_otp_secret(username: str, otp_secret: str):
    await db.users.update_one(
        {"username": username},
        {"$set": {"otp_secret": otp_secret, "otp_validated": False}},
    )


async def set_user_otp_secret_validated(username: str):
    await db.users.update_one(
        {"username": username},
        {"$set": {"otp_validated": True}},
    )
