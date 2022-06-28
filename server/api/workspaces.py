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
)
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
    return await get_workspaces_of_user(current_user.username)


# GET users of workspace
@router.get(
    "/workspace/users",
    response_model=list[WorkspaceUser],
    tags=["workspace"],
)
async def get_workspace_users(
    name: str, current_user: User = Depends(get_current_active_user)
):
    """
    Get all users for a workspace
    """
    # user needs to be in workspace
    await _assert_workspace_access(current_user.username, name)
    return await get_users_of_workspace(name)


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
    workspace = Workspace(
        name=name, admin=current_user.username, users=[current_user.username]
    )
    try:
        await create_workspace(workspace)
        return await get_workspace(name)
    except UniqueConstraintFailedException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workspace name already exists",
        )


# POST change workspace name
@router.post("/workspace/rename", response_model=Workspace, tags=["workspace"])
async def rename_workspace(
    old_name: str, new_name: str, current_user: User = Depends(get_current_active_user)
):

    await _assert_workspace_access_admin(current_user.username, old_name)

    try:
        await change_workspace_name(old_name, new_name)
        return await get_workspace(new_name)
    except UniqueConstraintFailedException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workspace name already exists",
        )


# POST add user to workspace todo test
@router.post("/workspace/add", response_model=Workspace, tags=["workspace"])
async def add_to_workspace(
    username: str, workspace: str, current_user: User = Depends(get_current_active_user)
):

    await _assert_user_exists(username)
    await _assert_workspace_access_admin(current_user.username, workspace)

    if not await is_user_in_workspace(username, workspace):
        await add_user_to_workspace(username, workspace)
    return await get_workspace(workspace)


# POST remove user from workspace todo test
@router.post("/workspace/remove", response_model=Workspace, tags=["workspace"])
async def remove_from_workspace(
    username: str, workspace: str, current_user: User = Depends(get_current_active_user)
):

    await _assert_user_exists(username)
    await _assert_workspace_access_admin(current_user.username, workspace)

    if await is_user_in_workspace(username, workspace):
        await remove_user_from_workspace(username, workspace)
    return await get_workspace(workspace)


# POST set another user as admin todo test
@router.post("/workspace/changeAdmin", response_model=Workspace, tags=["workspace"])
async def change_admin(
    username: str, workspace: str, current_user: User = Depends(get_current_active_user)
):

    await _assert_user_exists(username)
    await _assert_workspace_access_admin(current_user.username, workspace)

    if not await is_user_in_workspace(username, workspace):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in workspace.",
        )

    await change_workspace_admin(workspace, username)
    return await get_workspace(workspace)


# POST invite user to workspace
# todo


async def _assert_workspace_access(username: str, workspace: str):
    if not await is_user_in_workspace(username, workspace):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not in workspace.",
        )


async def _assert_workspace_access_admin(username: str, workspace: str):
    if not await is_user_admin_of_workspace(username, workspace):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin.",
        )


async def _assert_user_exists(username: str):
    if not await user_exists(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist.",
        )
