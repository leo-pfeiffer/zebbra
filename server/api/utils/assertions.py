from fastapi import HTTPException
from starlette import status

from core.dao.models import model_exists, has_access_to_model, is_admin, is_editor
from core.dao.users import user_exists
from core.dao.workspaces import (
    is_user_in_workspace,
    is_user_admin_of_workspace,
    workspace_exists,
)
from core.objects import PyObjectId


async def assert_workspace_access(user_id: PyObjectId, workspace_id: PyObjectId | str):
    if not await is_user_in_workspace(user_id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not in workspace.",
        )


async def assert_workspace_access_admin(user_id: PyObjectId, workspace_id: PyObjectId):
    if not await is_user_admin_of_workspace(user_id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin.",
        )


async def assert_workspace_exists(workspace_id: PyObjectId):
    if not await workspace_exists(workspace_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace does not exist.",
        )


async def assert_user_exists(user_id: PyObjectId):
    if not await user_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist.",
        )


async def assert_model_exists(model_id: str):
    if not await model_exists(model_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model does not exist.",
        )


async def assert_model_access(user_id: PyObjectId, model_id: str):
    if not await has_access_to_model(model_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to this model.",
        )


async def assert_model_access_admin(user_id: PyObjectId, model_id: str):
    if not await is_admin(model_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin.",
        )


async def assert_model_access_can_edit(user_id: PyObjectId, model_id: str):
    if not await is_admin(model_id, user_id) and not await is_editor(model_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User cannot edit this model.",
        )
