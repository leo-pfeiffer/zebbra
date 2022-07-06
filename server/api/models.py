from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.utils.assertions import (
    assert_model_access,
    assert_model_exists,
    assert_model_access_can_edit,
    assert_model_access_admin,
)
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
    update_sheet_meta_in_model,
    update_sheet_sections_in_model,
    get_sheet_by_name,
    is_editor,
    model_exists,
    remove_admin_from_model,
    get_users_for_model,
    get_revenues_sheet,
    get_costs_sheet,
    update_revenues_sheet,
    update_costs_sheet,
)
from core.dao.workspaces import is_user_in_workspace
from core.exceptions import (
    DoesNotExistException,
    NoAccessException,
    CardinalityConstraintFailedException,
    BusinessLogicException,
)
from core.objects import PyObjectId
from core.schemas.models import Model, ModelUser
from core.schemas.sheets import SheetMeta, Section, Sheet
from core.schemas.users import User
from core.schemas.utils import Message
from api.utils.dependencies import get_current_active_user

router = APIRouter()


@router.get(
    "/model",
    response_model=list[Model],
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def retrieve_list_of_models(
    model_id: str | None = None,
    workspace_id: PyObjectId | None = None,
    user: bool = False,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve models. The endpoint takes three **mutually exclusive** parameters:\n
        model_id: retrieve a list of a single model by its ID
        user: retrieve a list of all models of the current user
        workspace: retrieve a list of all models of a workspace
    """

    # assert that only one parameter has been specified
    if (model_id is not None) + (workspace_id is not None) + user != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exactly one of the query parameters must be specified.",
        )

    if model_id is not None:
        await assert_model_exists(model_id)
        await assert_model_access(current_user.id, model_id)
        models = [await get_model_by_id(model_id)]
        return models

    if workspace_id is not None:
        if not await is_user_in_workspace(current_user.id, workspace_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access to this workspace.",
            )
        return await get_models_for_workspace(workspace_id)

    if user:
        return await get_models_for_user(current_user.id)


# GET users of workspace
@router.get(
    "/model/users",
    response_model=list[ModelUser],
    tags=["model"],
)
async def retrieve_users_with_access_to_model(
    model_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a list of users that can access a model.\n
        model_id: ID of the model whose users to retrieve
    """
    # model must exist
    await _assert_model_exists(model_id)
    # user must be in workspace
    await _assert_access(current_user.id, model_id)
    return await get_users_for_model(model_id)


@router.post(
    "/model/grant",
    response_model=Message,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def grant_permission_for_model(
    model_id: str,
    role: Literal["admin", "editor", "viewer"],
    user_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    """
    Grant a permission to a user for a model.\n
        model_id: Model for which to give permission to
        role: Permission to be granted ["admin", "editor", "viewer"]
        user_id: User to whom the permission is granted
    """
    await assert_model_exists(model_id)

    # granting user must be admin
    await assert_model_access_admin(current_user.id, model_id)

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
async def revoke_permission_for_model(
    model_id: str,
    role: Literal["admin", "editor", "viewer"],
    user_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    """
    Revoke a permission from a user for a model.\n
        model_id: Model for which to revoke permission from
        role: Permission to be revoked ["admin", "editor", "viewer"]
        user_id: User from whom the permission is revoked
    """
    await _assert_model_exists(model_id)
    await assert_model_exists(model_id)

    # granting user must be admin
    await assert_model_access_admin(current_user.id, model_id)

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
async def rename_existing_model(
    model_id: str,
    name: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Rename a model.\n
        model_id: Model to rename
        name: The new name for the model
    """
    await _assert_model_exists(model_id)
    # only editor can rename
    await assert_model_access_can_edit(current_user.id, model_id)
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
async def create_new_model(
    name: str,
    workspace_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new model with the current user as admin.\n
        name: Name of the new model
        workspace_id: ID of the workspace to which the workspace belongs
    """
    try:
        r = await create_model(current_user.id, name, workspace_id)
        return await get_model_by_id(r.inserted_id)
    except NoAccessException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not in the workspace.",
        )


@router.get(
    "/model/revenues",
    response_model=Sheet,
    tags=["model"],
    responses={
        400: {"description": "Model does not exist."},
        403: {"description": "User does not have access to the resource."},
    },
)
async def retrieve_model_sheet_revenues(
    model_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve the 'Revenues' sheet of a model.\n
        model_id: Model for which to retrieve the sheet
    """
    await _assert_model_exists(model_id)
    await _assert_access(current_user.id, model_id)

    return await get_revenues_sheet(model_id)


@router.post(
    "/model/revenues",
    response_model=Sheet,
    tags=["model"],
    responses={
        400: {"description": "Model does not exist."},
        403: {"description": "User does not have access to the resource."},
    },
)
async def update_model_sheet_revenues(
    model_id: str,
    sheet_data: Sheet,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update the 'Revenues' sheet of a model.\n
        model_id: Model for which to update the sheet
        sheet_data: New data of the sheet
    """
    await _assert_model_exists(model_id)
    # only editor can update sheet
    await _assert_access_can_edit(current_user.id, model_id)

    assert sheet_data.meta.name == "Revenues"  # todo test, refactor

    await update_revenues_sheet(model_id, sheet_data)
    return await get_revenues_sheet(model_id)


@router.get(
    "/model/costs",
    response_model=Sheet,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def retrieve_model_sheet_costs(
    model_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve the 'Costs' sheet of a model.\n
        model_id: Model for which to retrieve the sheet
    """
    await _assert_model_exists(model_id)
    await _assert_access(current_user.id, model_id)

    return await get_costs_sheet(model_id)


@router.post(
    "/model/costs",
    response_model=Sheet,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def update_model_sheet_costs(
    model_id: str,
    sheet_data: Sheet,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update the 'Costs' sheet of a model.\n
        model_id: Model for which to update the sheet
        sheet_data: New data of the sheet
    """
    await _assert_model_exists(model_id)
    # only editor can update sheet
    await _assert_access_can_edit(current_user.id, model_id)

    assert sheet_data.meta.name == "Costs"  # todo test, refactor

    await update_costs_sheet(model_id, sheet_data)
    return await get_costs_sheet(model_id)


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
