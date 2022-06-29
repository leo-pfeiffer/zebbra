from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.dao.models import (
    has_access_to_model,
    get_model_by_id,
    get_models_for_workspace,
    get_models_for_user,
    add_admin_to_model,
    add_editor_to_model,
    add_viewer_to_model,
    remove_viewer_from_model,
    remove_editor_from_model,
    is_admin,
    set_name,
    create_model,
    is_editor,
    update_sheet_meta_in_model,
    update_sheet_sections_in_model,
    model_exists,
    get_sheet_by_name,
    remove_admin_from_model,
    get_users_for_model,
)
from core.dao.workspaces import is_user_in_workspace
from core.exceptions import (
    DoesNotExistException,
    NoAccessException,
    UniqueConstraintFailedException,
    CardinalityConstraintFailedException,
    BusinessLogicException,
)
from core.objects import PyObjectId
from core.schemas.models import Model, ModelUser
from core.schemas.sheets import SheetMeta, Section, Sheet
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
    },
)
async def get_model(
    model_id: str | None = None,
    workspace: str | None = None,
    user: bool = False,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve models:
        model_id: model with the id,
        workspace: models of a workspace,
        user: models of the current user.
    """

    # assert that only one parameter has been specified
    if (model_id is not None) + (workspace is not None) + user != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exactly one of the query parameters must be specified.",
        )

    if model_id is not None:
        await _assert_model_exists(model_id)
        await _assert_access(current_user.id, model_id)
        return [await get_model_by_id(model_id)]

    if workspace is not None:
        if not await is_user_in_workspace(current_user.id, workspace):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access to this workspace.",
            )
        return await get_models_for_workspace(workspace)

    if user:
        return await get_models_for_user(current_user.id)


@router.post(
    "/model/grant",
    response_model=Message,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def model_grant_permission(
    model_id: str,
    role: Literal["admin", "editor", "viewer"],
    user_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    await _assert_model_exists(model_id)

    # granting user must be admin
    await _assert_access_admin(current_user.id, model_id)

    try:
        if role == "admin":
            await add_admin_to_model(user_id, model_id)

        elif role == "editor":
            await add_editor_to_model(user_id, model_id)

        elif role == "viewer":
            await add_viewer_to_model(user_id, model_id)

        return {"message": f"Access granted ({role})"}

    except DoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist.",
        )


@router.post(
    "/model/revoke",
    response_model=Message,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def model_revoke_permission(
    model_id: str,
    role: Literal["admin", "editor", "viewer"],
    user_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    await _assert_model_exists(model_id)

    # granting user must be admin
    await _assert_access_admin(current_user.id, model_id)

    try:
        if role == "admin":
            try:
                await remove_admin_from_model(user_id, model_id)
            except CardinalityConstraintFailedException:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Each model must have at least one admin.",
                )
            except BusinessLogicException:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot remove workspace admin from model.",
                )

        elif role == "editor":
            await remove_editor_from_model(user_id, model_id)

        elif role == "viewer":
            await remove_viewer_from_model(user_id, model_id)

        return {"message": f"Access revoked ({role})"}

    except DoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist.",
        )


@router.post(
    "/model/rename",
    response_model=Message,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def model_rename(
    model_id: str,
    name: str,
    current_user: User = Depends(get_current_active_user),
):
    await _assert_model_exists(model_id)
    # only editor can rename
    await _assert_access_can_edit(current_user.id, model_id)
    await set_name(model_id, name)
    return {"message": f"Model renamed ({name})"}


@router.post(
    "/model/add",
    response_model=Model,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def model_add(
    name: str,
    workspace: str,
    current_user: User = Depends(get_current_active_user),
):
    try:
        r = await create_model(current_user.id, name, workspace)
        return await get_model_by_id(r.inserted_id)
    except NoAccessException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not in the workspace.",
        )


@router.post(
    "/model/sheet/update/data",
    response_model=Sheet,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def update_sheet_data(
    model_id: str,
    name: str,
    sheet_data: list[Section],
    current_user: User = Depends(get_current_active_user),
):
    await _assert_model_exists(model_id)
    # only editor can update sheet
    await _assert_access_can_edit(current_user.id, model_id)
    await update_sheet_sections_in_model(model_id, name, sheet_data)
    return await get_sheet_by_name(model_id, name)


@router.post(
    "/model/sheet/update/meta",
    response_model=Sheet,
    tags=["model"],
    responses={
        400: {"description": "Sheet does not exist."},
        403: {"description": "User does not have access to the resource."},
        409: {"description": "Sheet name already exists in the same model."},
    },
)
async def update_sheet_meta(
    model_id: str,
    name: str,
    sheet_meta: SheetMeta,
    current_user: User = Depends(get_current_active_user),
):
    await _assert_model_exists(model_id)
    # only editor can update sheet
    await _assert_access_can_edit(current_user.id, model_id)
    try:
        await update_sheet_meta_in_model(model_id, name, sheet_meta)
        return await get_sheet_by_name(model_id, sheet_meta.name)
    except UniqueConstraintFailedException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sheet name already exists in the same model.",
        )


# GET users of workspace
@router.get(
    "/model/users",
    response_model=list[ModelUser],
    tags=["model"],
)
async def get_model_users(
    model_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Get all users for a workspace
    """
    # model must exist
    await _assert_model_exists(model_id)
    # user must be in workspace
    await _assert_access(current_user.id, model_id)
    return await get_users_for_model(model_id)


async def _assert_model_exists(model_id: str):
    if not await model_exists(model_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model does not exist.",
        )


async def _assert_access(user_id: PyObjectId, model_id: str):
    if not await has_access_to_model(model_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to this model.",
        )


async def _assert_access_admin(user_id: PyObjectId, model_id: str):
    if not await is_admin(model_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin.",
        )


async def _assert_access_can_edit(user_id: PyObjectId, model_id: str):
    if not await is_admin(model_id, user_id) and not await is_editor(model_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User cannot edit this model.",
        )
