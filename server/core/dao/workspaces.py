from fastapi.encoders import jsonable_encoder

from core.exceptions import UniqueConstraintFailedException, DoesNotExistException
from core.dao.database import db
from core.dao.users import get_user
from core.schemas.workspaces import Workspace


async def get_workspace(name: str):
    """
    Get a workspace by its name
    :param name: name of the workspace
    """
    workspace = await db.workspaces.find_one({"name": name})
    if workspace is not None:
        return Workspace(**workspace)


async def get_workspaces_of_user(username: str):
    """
    Return a list of all workspaces that the user is a member of
    :param username: username of the user
    """
    num = await db.workspaces.count_documents({"users": username})
    cursor = db.workspaces.find({"users": username})
    lis = [Workspace(**w) for w in await cursor.to_list(length=num)]
    return lis


async def get_admin_workspaces_of_user(username: str):
    """
    Return a list of the workspaces of which the user is the admin.
    :param username: username of the admin
    """
    num = await db.workspaces.count_documents({"admin": username})
    cursor = db.workspaces.find({"admin": username})
    lis = [Workspace(**w) for w in await cursor.to_list(length=num)]
    return lis


async def create_workspace(workspace: Workspace):
    """
    Create a new workspace.
    """
    if await get_workspace(workspace.name) is not None:
        raise UniqueConstraintFailedException("Username must be unique")
    return await db.workspaces.insert_one(jsonable_encoder(workspace))


async def change_workspace_admin(workspace: str, username: str):
    """
    Change the admin of the workspace to the user with the given username.
    :param workspace: the workspace whose admin to change
    :param username: the username of the new admin
    """
    if await get_user(username) is None:
        raise DoesNotExistException("User does not exist")

    await db.workspaces.update_one({"name": workspace}, {"$set": {"admin": username}})
