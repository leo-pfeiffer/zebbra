from fastapi.encoders import jsonable_encoder

from core.exceptions import UniqueConstraintFailedException, DoesNotExistException
from core.dao.database import db
from core.dao.users import get_user
from core.schemas.workspaces import Workspace, WorkspaceUser


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


async def get_users_of_workspace(workspace: str):
    # get unique users
    wsp = await get_workspace(workspace)
    if wsp is None:
        raise DoesNotExistException("Workspace does not exist")

    usernames = list(set(wsp.users))
    users = []
    admins = []
    for username in usernames:
        user = await get_user(username)
        user_role = "Admin" if username == wsp.admin else "Member"
        wsp_user = WorkspaceUser(
            username=username,
            first_name=user.first_name,
            last_name=user.last_name,
            user_role=user_role,
        )
        if username == wsp.admin:
            admins.append(wsp_user)
        else:
            users.append(wsp_user)

    admins.sort(key=lambda x: x.last_name)
    users.sort(key=lambda x: x.last_name)
    return admins + users


async def is_user_in_workspace(username: str, workspace: str):
    """
    Returns true if the user is in the workspace, else false.
    :param username: username of the user
    :param workspace: workspace name
    """
    return (
        await db.workspaces.count_documents(
            {"name": workspace, "$or": [{"admin": username}, {"users": username}]}
        )
        > 0
    )


async def is_user_admin_of_workspace(username: str, workspace: str):
    """
    Returns true if the user is the admin of the workspace, else false.
    :param username: username of the user
    :param workspace: workspace name
    """
    return (
        await db.workspaces.count_documents({"name": workspace, "admin": username}) > 0
    )


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
        raise UniqueConstraintFailedException("Workspace name must be unique")
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

    # add the new admin as admin to all models of the workspace
    await db.models.update_many(
        {"meta.workspace": workspace, "meta.admins": {"$ne": username}},
        {"$push": {"meta.admins": username}},
    )


async def change_workspace_name(old_name: str, new_name: str):
    """
    Change the workspace name.
    """
    if await get_workspace(new_name) is not None:
        raise UniqueConstraintFailedException("Workspace name must be unique")

    await db.workspaces.update_one({"name": old_name}, {"$set": {"name": new_name}})

    # change users
    await db.users.update_many(
        {"workspaces": old_name}, {"$push": {"workspaces": new_name}}
    )

    await db.users.update_many(
        {"workspaces": old_name}, {"$pull": {"workspaces": old_name}}
    )

    # change models
    await db.models.update_many(
        {"workspace": old_name}, {"$set": {"workspace": new_name}}
    )
