from fastapi.encoders import jsonable_encoder

from core.exceptions import UniqueConstraintFailedException
from core.models.database import db
from core.schemas.workspaces import Workspace


async def get_workspace(name: str):
    workspace = await db["workspaces"].find_one({"name": name})
    if workspace is not None:
        return Workspace(**workspace)


async def get_workspaces_of_user(username: str):
    num = await db["workspaces"].count_documents({"users": username})
    cursor = db["workspaces"].find({"users": username})
    lis = [Workspace(**w) for w in await cursor.to_list(length=num)]
    return lis


async def create_workspace(workspace: Workspace):
    if await get_workspace(workspace.name) is not None:
        raise UniqueConstraintFailedException("Username must be unique")
    return await db["workspaces"].insert_one(jsonable_encoder(workspace))
