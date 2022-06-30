from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.dao.users import (
    add_user_to_workspace,
    remove_user_from_workspace,
    user_exists,
)
from core.dao.workspaces import (
    is_user_in_workspace,
    get_workspaces_of_user,
    create_workspace,
    get_workspace,
    change_workspace_name,
    is_user_admin_of_workspace,
    change_workspace_admin,
    get_users_of_workspace,
)
from core.exceptions import (
    UniqueConstraintFailedException,
    BusinessLogicException,
)
from core.objects import PyObjectId
from core.schemas.users import User
from core.schemas.workspaces import Workspace, WorkspaceUser
from dependencies import get_current_active_user

router = APIRouter()


# GET workspace
@router.get(
    "/workspace",
    response_model=list[Workspace],
    tags=["workspace"],
)
async def get_workspace_for_user(current_user: User = Depends(get_current_active_user)):
    """
    Get all workspaces for the logged-in user.
    """
    return await get_workspaces_of_user(current_user.id)


# GET users of workspace
@router.get(
    "/workspace/users",
    response_model=list[WorkspaceUser],
    tags=["workspace"],
)
async def get_workspace_users(
    workspace_id: PyObjectId, current_user: User = Depends(get_current_active_user)
):
    """
    Get all users for a workspace
    """
    # user needs to be in workspace
    await _assert_workspace_access(current_user.id, workspace_id)
    return await get_users_of_workspace(workspace_id)


# CREATE workspace
@router.post(
    "/workspace",
    response_model=Workspace,
    tags=["workspace"],
)
async def create_new_workspace(
    name: str, current_user: User = Depends(get_current_active_user)
):
    """
    Create a new workspace with the current user as admin.
    """
    workspace = Workspace(name=name, admin=current_user.id, users=[current_user.id])
    try:
        obj = await create_workspace(workspace)
        return await get_workspace(obj.inserted_id)
    except UniqueConstraintFailedException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workspace name already exists",
        )


# POST change workspace name
@router.post("/workspace/rename", response_model=Workspace, tags=["workspace"])
async def rename_workspace(
    workspace_id: PyObjectId,
    new_name: str,
    current_user: User = Depends(get_current_active_user),
):
    await _assert_workspace_access_admin(current_user.id, workspace_id)

    try:
        await change_workspace_name(workspace_id, new_name)
        return await get_workspace(workspace_id)
    except UniqueConstraintFailedException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workspace name already exists",
        )


# POST add user to workspace todo test
@router.post("/workspace/add", response_model=Workspace, tags=["workspace"])
async def add_to_workspace(
    user_id: PyObjectId,
    workspace_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    await _assert_user_exists(user_id)
    await _assert_workspace_access_admin(current_user.id, workspace_id)

    if not await is_user_in_workspace(user_id, workspace_id):
        await add_user_to_workspace(user_id, workspace_id)
    return await get_workspace(workspace_id)


# POST remove user from workspace todo test
@router.post("/workspace/remove", response_model=Workspace, tags=["workspace"])
async def remove_from_workspace(
    user_id: PyObjectId,
    workspace_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    await _assert_user_exists(user_id)
    await _assert_workspace_access_admin(current_user.id, workspace_id)

    if await is_user_in_workspace(user_id, workspace_id):
        try:
            await remove_user_from_workspace(user_id, workspace_id)
        except BusinessLogicException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove user due to business logic violation.",
            )

    return await get_workspace(workspace_id)


# POST set another user as admin todo test
@router.post("/workspace/changeAdmin", response_model=Workspace, tags=["workspace"])
async def change_admin(
    user_id: PyObjectId,
    workspace_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    await _assert_user_exists(user_id)
    await _assert_workspace_access_admin(current_user.id, workspace_id)

    if not await is_user_in_workspace(user_id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in workspace.",
        )

    await change_workspace_admin(workspace_id, user_id)
    return await get_workspace(workspace_id)


# POST invite user to workspace
# todo


async def _assert_workspace_access(user_id: PyObjectId, workspace_id: PyObjectId):
    if not await is_user_in_workspace(user_id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not in workspace.",
        )


async def _assert_workspace_access_admin(user_id: PyObjectId, workspace_id: PyObjectId):
    if not await is_user_admin_of_workspace(user_id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin.",
        )


async def _assert_user_exists(user_id: PyObjectId):
    if not await user_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist.",
        )
