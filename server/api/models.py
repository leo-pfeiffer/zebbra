from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.dao.models import (
    has_access_to_model,
    get_model_by_id,
    get_models_for_workspace,
    get_models_for_user,
)
from core.dao.workspaces import is_user_in_workspace
from core.schemas.models import Model
from core.schemas.sheets import Sheet
from core.schemas.users import User
from core.types import ModelPermissionTypes
from dependencies import get_current_active_user

router = APIRouter()

# Todo:
#  As of now, almost all endpoints return the current model. This could make it easier
#  to use the result of the API call. However, I could also return Messages instead.


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
        if not await has_access_to_model(id, current_user.username):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access to this model.",
            )
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


@router.post(
    "/model/grant",
    response_model=Model,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
        400: {"description": "Missing parameters."},
    },
)
async def model_grant_permission(
    id: str,
    role: ModelPermissionTypes,
    user: str,
    current_user: User = Depends(get_current_active_user),
):
    # todo
    ...


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
