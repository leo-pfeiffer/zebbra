from fastapi.encoders import jsonable_encoder

from core.exceptions import UniqueConstraintFailedException, DoesNotExistException
from core.dao.database import db
from core.dao.users import get_user, user_exists
from core.schemas.models import create_new_demo_model, Model
from core.schemas.utils import PyObjectId
from core.schemas.workspaces import Workspace, WorkspaceUser


async def workspace_exists(workspace_id: PyObjectId):
    return await get_workspace(workspace_id) is not None


async def workspace_name_exists(workspace_name: str):
    return await get_workspace_by_name(workspace_name) is not None


async def get_workspace(workspace_id: PyObjectId):
    """
    Get a workspace by its name
    :param workspace_id: name of the workspace
    """
    workspace = await db.workspaces.find_one({"_id": str(workspace_id)})
    if workspace is not None:
        return Workspace(**workspace)


async def get_workspace_by_name(name: str):
    """
    Get a workspace by its name
    :param name: name of the workspace
    """
    workspace = await db.workspaces.find_one({"name": name})
    if workspace is not None:
        return Workspace(**workspace)


async def get_workspaces_of_user(user_id: PyObjectId):
    """
    Return a list of all workspaces that the user is a member of
    :param user_id: user id of the user
    """
    num = await db.workspaces.count_documents({"users": str(user_id)})
    cursor = db.workspaces.find({"users": str(user_id)})
    lis = [Workspace(**w) for w in await cursor.to_list(length=num)]
    return lis


async def get_users_of_workspace(workspace_id: PyObjectId):
    # get unique users
    wsp = await get_workspace(workspace_id)
    if wsp is None:
        raise DoesNotExistException("Workspace does not exist")

    user_set = set(wsp.users)
    user_set.add(wsp.admin)
    user_ids = list(user_set)
    users = []
    admins = []

    for user_id in user_ids:
        user = await get_user(user_id)
        user_role = "Admin" if user_id == wsp.admin else "Member"
        wsp_user = WorkspaceUser(
            _id=str(user.id),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            user_role=user_role,
        )
        if user_id == wsp.admin:
            admins.append(wsp_user)
        else:
            users.append(wsp_user)

    admins.sort(key=lambda x: x.last_name)
    users.sort(key=lambda x: x.last_name)
    return admins + users


async def is_user_in_workspace(user_id: PyObjectId, workspace_id: PyObjectId):
    """
    Returns true if the user is in the workspace, else false.
    :param user_id: user id of the user
    :param workspace_id: workspace name
    """
    return (
        await db.workspaces.count_documents(
            {
                "_id": str(workspace_id),
                "$or": [{"admin": str(user_id)}, {"users": str(user_id)}],
            }
        )
        > 0
    )


async def is_user_admin_of_workspace(user_id: PyObjectId, workspace_id: PyObjectId):
    """
    Returns true if the user is the admin of the workspace, else false.
    :param user_id: user id of the user
    :param workspace_id: workspace id
    """
    return (
        await db.workspaces.count_documents(
            {"_id": str(workspace_id), "admin": str(user_id)}
        )
        > 0
    )


async def get_admin_workspaces_of_user(user_id: PyObjectId):
    """
    Return a list of the workspaces of which the user is the admin
    :param user_id: user id of the admin
    """
    num = await db.workspaces.count_documents({"admin": str(user_id)})
    cursor = db.workspaces.find({"admin": str(user_id)})
    lis = [Workspace(**w) for w in await cursor.to_list(length=num)]
    return lis


async def create_workspace(workspace: Workspace):
    """
    Create a new workspace.
    """
    if await get_workspace_by_name(workspace.name) is not None:
        raise UniqueConstraintFailedException("Workspace name must be unique")

    # insert the demo model
    demo_model = await get_demo_model()
    model = create_new_demo_model(workspace.admin, workspace.id, demo_model)
    await db.models.insert_one(jsonable_encoder(model))

    return await db.workspaces.insert_one(jsonable_encoder(workspace))


async def change_workspace_admin(workspace_id: PyObjectId, user_id: PyObjectId):
    """
    Change the admin of the workspace to the user with the given username
    :param workspace_id: the workspace id whose admin to change
    :param user_id: the user id of the new admin
    """
    if not await user_exists(user_id):
        raise DoesNotExistException("User does not exist")

    await db.workspaces.update_one(
        {"_id": str(workspace_id)}, {"$set": {"admin": str(user_id)}}
    )

    # add the new admin as admin to all models of the workspace
    await db.models.update_many(
        {"meta.workspace": str(workspace_id), "meta.admins": {"$ne": str(user_id)}},
        {"$push": {"meta.admins": str(user_id)}},
    )


async def change_workspace_name(workspace_id: PyObjectId, new_name: str):
    """
    Change the workspace name.
    """
    if await get_workspace_by_name(new_name) is not None:
        raise UniqueConstraintFailedException("Workspace name must be unique")

    await db.workspaces.update_one(
        {"_id": str(workspace_id)}, {"$set": {"name": new_name}}
    )

    # change models
    await db.models.update_many(
        {"workspace": str(workspace_id)}, {"$set": {"workspace": new_name}}
    )


async def add_user_to_workspace(user_id: PyObjectId, workspace_id: PyObjectId):
    if not await is_user_in_workspace(user_id, workspace_id):
        # add user to workspace
        return await db.workspaces.update_one(
            {"_id": str(workspace_id)}, {"$push": {"users": str(user_id)}}
        )


async def get_demo_model() -> Model:
    demo_model = await db.demo.find_one({})
    if demo_model:
        return Model(**demo_model)
