from datetime import timedelta, datetime

import pyotp
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.utils.assertions import (
    assert_workspace_access_admin,
    assert_user_exists,
    assert_workspace_access,
)
from core.dao.invite_codes import add_invite_code
from core.dao.users import (
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
    add_user_to_workspace,
)
from core.exceptions import (
    UniqueConstraintFailedException,
    BusinessLogicException,
)
from core.schemas.users import User
from core.schemas.utils import InviteCode, PyObjectId
from core.schemas.workspaces import Workspace, WorkspaceUser
from api.utils.dependencies import get_current_active_user, INVITE_CODE_EXPIRES_MINUTES

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


@router.get(
    "/workspace/users",
    response_model=list[WorkspaceUser],
    tags=["workspace"],
)
async def list_workspace_users(
    workspace_id: PyObjectId, current_user: User = Depends(get_current_active_user)
):
    """
    Get all users for a workspace.\n
        :workspace_id: ID of the workspace
    """
    # user needs to be in workspace
    await assert_workspace_access(current_user.id, workspace_id)
    return await get_users_of_workspace(workspace_id)


@router.post(
    "/workspace",
    response_model=Workspace,
    tags=["workspace"],
)
async def create_new_workspace(
    name: str, current_user: User = Depends(get_current_active_user)
):
    """
    Create a new workspace with the current user as admin.\n
        name: name of the workspace
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
    """
    Rename a workspace.\n
        workspace_id: ID of the workspace to rename.
        new_name: New name for the workspace.
    """
    await assert_workspace_access_admin(current_user.id, workspace_id)

    try:
        await change_workspace_name(workspace_id, new_name)
        return await get_workspace(workspace_id)
    except UniqueConstraintFailedException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workspace name already exists",
        )


# POST add user to workspace
@router.post("/workspace/add", response_model=Workspace, tags=["workspace"])
async def add_user_to_a_workspace(
    user_id: PyObjectId,
    workspace_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    """
    Add a user to a workspace.\n
        user_id: ID of the user to add.
        workspace_id: ID of the workspace to add the user to.
    """
    await assert_user_exists(user_id)
    await assert_workspace_access_admin(current_user.id, workspace_id)

    if not await is_user_in_workspace(user_id, workspace_id):
        await add_user_to_workspace(user_id, workspace_id)
    return await get_workspace(workspace_id)


# POST remove user from workspace
@router.post("/workspace/remove", response_model=Workspace, tags=["workspace"])
async def remove_user_from_a_workspace(
    user_id: PyObjectId,
    workspace_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    """
    Remove a user from a workspace.\n
        user_id: ID of the user to remove.
        workspace_id: ID of the workspace to remove the user from.
    """
    await assert_user_exists(user_id)
    await assert_workspace_access_admin(current_user.id, workspace_id)

    if await is_user_in_workspace(user_id, workspace_id):
        try:
            await remove_user_from_workspace(user_id, workspace_id)
        except BusinessLogicException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove user due to business logic violation.",
            )

    return await get_workspace(workspace_id)


# POST set another user as admin
@router.post("/workspace/changeAdmin", response_model=Workspace, tags=["workspace"])
async def set_admin_of_workspace(
    user_id: PyObjectId,
    workspace_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    """
    Set another user as admin of a workspace.\n
        user_id: ID of the user to set as admin.
        workspace_id: ID of the workspace to set the admin for.
    """
    await assert_user_exists(user_id)
    await assert_workspace_access_admin(current_user.id, workspace_id)

    if not await is_user_in_workspace(user_id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in workspace.",
        )

    await change_workspace_admin(workspace_id, user_id)
    return await get_workspace(workspace_id)


@router.post("/workspace/inviteCode", response_model=InviteCode, tags=["workspace"])
async def create_invite_code_for_workspace(
    workspace_id: PyObjectId, current_user: User = Depends(get_current_active_user)
):
    """
    Create an invite code for a workspace.\n
        workspace_id: ID of the workspace to create the invite code for.
    """
    await assert_workspace_access_admin(current_user.id, workspace_id)

    invite_code = pyotp.random_base32()
    invite_code_expires = datetime.utcnow() + timedelta(
        minutes=INVITE_CODE_EXPIRES_MINUTES
    )

    obj = InviteCode(
        invite_code=invite_code,
        workspace_id=str(workspace_id),
        expires=invite_code_expires,
    )

    await add_invite_code(obj)

    return obj


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
