from fastapi import APIRouter, Depends, HTTPException
from typing import Literal
from starlette import status

from core.dao.models import (
    has_access_to_model,
    get_model_by_id,
    get_models_for_workspace,
    get_models_for_user,
    set_admin,
    add_editor_to_model,
    add_viewer_to_model,
    remove_viewer_from_model,
    remove_editor_from_model,
    is_admin,
)
from core.dao.workspaces import is_user_in_workspace
from core.exceptions import DoesNotExistException
from core.schemas.models import Model
from core.schemas.sheets import Sheet
from core.schemas.users import User
from core.schemas.utils import Message
from dependencies import get_current_active_user

router = APIRouter()


@router.get(
    "/model",
    response_model=list[Model],
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
        400: {"description": "Exactly one of the query parameters must be specified."},
    },
)
async def get_model(
    id: str | None = None,
    workspace: str | None = None,
    user: bool = False,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve models:
        id: model with the id,
        workspace: models of a workspace,
        user: models of the current user.
    """

    # assert that only one parameter has been specified
    if (id is not None) + (workspace is not None) + user != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exactly one of the query parameters must be specified.",
        )

    if id is not None:
        await _assert_access(current_user.username, id)
        return [await get_model_by_id(id)]

    if workspace is not None:
        if not await is_user_in_workspace(current_user.username, workspace):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access to this workspace.",
            )
        return await get_models_for_workspace(workspace)

    if user:
        return await get_models_for_user(current_user.username)


# todo test
@router.post(
    "/model/grant",
    response_model=Message,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
        400: {"description": "User does not exist."},
    },
)
async def model_grant_permission(
    id: str,
    role: Literal["admin", "editor", "viewer"],
    user: str,
    current_user: User = Depends(get_current_active_user),
):
    # granting user must have access
    await _assert_access_admin(current_user.username, id)

    try:
        if role == "admin":
            await set_admin(user, id)

        elif role == "editor":
            await add_editor_to_model(user, id)

        elif role == "viewer":
            await add_viewer_to_model(user, id)

        return {"message": f"Access granted ({role})"}

    except DoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist.",
        )


# todo test
@router.post(
    "/model/revoke",
    response_model=Message,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
        400: {"description": "Missing parameters."},
    },
)
async def model_revoke_permission(
    id: str,
    role: Literal["editor", "viewer"],
    user: str,
    current_user: User = Depends(get_current_active_user),
):
    # granting user must have access
    await _assert_access_admin(current_user.username, id)

    try:
        if role == "editor":
            await remove_editor_from_model(user, id)

        elif role == "viewer":
            await remove_viewer_from_model(user, id)

        return {"message": f"Access revoked ({role})"}

    except DoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist.",
        )


@router.post(
    "/model/rename",
    response_model=Model,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
        400: {"description": "Missing parameters."},
    },
)
async def model_rename(
    id: str,
    name: str,
    current_user: User = Depends(get_current_active_user),
):
    # todo
    ...


@router.post(
    "/model/add",
    response_model=Model,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
        400: {"description": "Missing parameters."},
    },
)
async def model_add(
    name: str,
    workspace: str,
    current_user: User = Depends(get_current_active_user),
):
    # todo
    ...


@router.post(
    "/model/sheet/add",
    response_model=Model,
    tags=["model"],
    responses={
        400: {"description": "Missing parameters."},
        403: {"description": "User does not have access to the resource."},
        409: {"description": "Sheet name already exists in the same model."},
    },
)
async def add_sheet(
    id: str,
    name: str,
    current_user: User = Depends(get_current_active_user),
):
    # todo
    ...


@router.post(
    "/model/sheet/delete",
    response_model=Model,
    tags=["model"],
    responses={
        400: {"description": "Missing parameters."},
        403: {"description": "User does not have access to the resource."},
    },
)
async def delete_sheet(
    id: str,
    name: str,
    current_user: User = Depends(get_current_active_user),
):
    # todo
    ...


@router.post(
    "/model/sheet/update",
    response_model=Model,
    tags=["model"],
    responses={
        400: {"description": "Missing parameters."},
        403: {"description": "User does not have access to the resource."},
    },
)
async def delete_sheet(
    id: str,
    name: str,
    sheet: Sheet,
    current_user: User = Depends(get_current_active_user),
):
    # todo
    ...


async def _assert_access(username: str, model_id: str):
    if not await has_access_to_model(model_id, username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to this model.",
        )


async def _assert_access_admin(username: str, model_id: str):
    if not await is_admin(model_id, username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin.",
        )
