from datetime import date
from typing import Literal

from dateutil.relativedelta import relativedelta
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
    add_admin_to_model,
    add_editor_to_model,
    add_viewer_to_model,
    is_admin,
    set_name,
    create_model,
    is_editor,
    model_exists,
    get_users_for_model,
    get_revenues_sheet,
    get_costs_sheet,
    update_revenues_sheet,
    update_costs_sheet,
    set_starting_month,
    update_model_employees,
    delete_model,
    remove_user_from_model,
    set_starting_balance,
)
from core.exceptions import (
    DoesNotExistException,
    NoAccessException,
    CardinalityConstraintFailedException,
    BusinessLogicException,
)
from core.schemas.models import (
    Model,
    ModelUser,
    ModelMeta,
    Employee,
    Payroll,
    UpdateEmployee,
)
from core.schemas.sheets import Sheet
from core.schemas.users import User
from core.schemas.utils import Message, PyObjectId
from api.utils.dependencies import get_current_active_user
from core.integrations.merge import (
    merge_accounting_integration_data,
    merge_payroll_integration_data,
    aggregate_payroll_info,
)

router = APIRouter()


@router.get(
    "/model/meta",
    response_model=ModelMeta,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def retrieve_model_meta(
    model_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve metadata of a model.\n
        model_id: Id of the model whose meta data to retrieve
    """

    await assert_model_exists(model_id)
    await assert_model_access(current_user.id, model_id)
    model = await get_model_by_id(model_id)

    return model.meta


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

    except BusinessLogicException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot demote workspace admin.",
        )


@router.post(
    "/model/revoke",
    response_model=Message,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def revoke_all_permissions_for_model(
    model_id: str,
    user_id: PyObjectId,
    current_user: User = Depends(get_current_active_user),
):
    """
    Revoke all permissions from a user for a model.\n
        model_id: Model for which to revoke permission from
        user_id: User from whom the permission is revoked
    """
    await _assert_model_exists(model_id)
    await assert_model_exists(model_id)

    # granting user must be admin
    await assert_model_access_admin(current_user.id, model_id)

    try:
        try:
            await remove_user_from_model(user_id, model_id)
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

        return {"message": f"Access revoked."}

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
    "/model/startingMonth",
    response_model=Message,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def set_starting_month_of_model(
    model_id: str,
    starting_month: date,
    current_user: User = Depends(get_current_active_user),
):
    """
    Set the starting month of a model. The starting month is provided as a date\n
        model_id: Model whose starting month to change
        starting_month: New starting month
    """
    await _assert_model_exists(model_id)
    # only editor can set start month
    await assert_model_access_can_edit(current_user.id, model_id)
    await set_starting_month(model_id, starting_month)
    return {"message": f"Starting month set ({starting_month})"}


@router.post(
    "/model/startingBalance",
    response_model=Message,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def set_starting_balance_of_model(
    model_id: str,
    starting_balance: float,
    current_user: User = Depends(get_current_active_user),
):
    """
    Set the starting balance of a model.\n
        model_id: Model whose starting balance to change
        starting_balance: New starting month
    """
    await _assert_model_exists(model_id)
    # only editor can set balance
    await assert_model_access_can_edit(current_user.id, model_id)
    await set_starting_balance(model_id, starting_balance)
    return {"message": f"Starting balance set ({starting_balance})"}


@router.post(
    "/model/add",
    response_model=Model,
    tags=["model"],
    responses={
        400: {"description": "Workspace does not exist."},
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
    except DoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace does not exist.",
        )
    except NoAccessException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not in the workspace.",
        )


@router.delete(
    "/model/delete",
    response_model=Message,
    tags=["model"],
    responses={
        400: {"description": "Model does not exist."},
        403: {"description": "User is not admin."},
    },
)
async def delete_existing_model(
    model_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Delete an existing model\n
        model_id: Id of the model to be deleted.
    """
    # model must exist
    await assert_model_exists(model_id)

    # only admin can delete
    await assert_model_access_admin(user_id=current_user.id, model_id=model_id)

    # delete model
    await delete_model(model_id)
    return {"message": "Model successfully deleted."}


@router.get(
    "/model/revenues",
    response_model=Sheet,
    tags=["model"],
    responses={
        400: {"description": "Model does not exist."},
        403: {"description": "User does not have access to the resource."},
    },
)
async def retrieve_revenues_sheet_of_model(
    model_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve the 'Revenues' sheet of a model.\n
        model_id: Model for which to retrieve the sheet
    """
    # model must exist
    await _assert_model_exists(model_id)

    # user must have access to model
    await _assert_access(current_user.id, model_id)

    model = await get_model_by_id(model_id)
    sheet = await get_revenues_sheet(model_id)

    # merge the data from the integration
    return await merge_accounting_integration_data(
        sheet, str(model.meta.workspace), model.meta.starting_month
    )


@router.post(
    "/model/revenues",
    response_model=Sheet,
    tags=["model"],
    responses={
        400: {"description": "Model does not exist."},
        403: {"description": "User does not have access to the resource."},
    },
)
async def update_revenues_sheet_of_model(
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

    assert sheet_data.meta.name == "Revenues"

    await update_revenues_sheet(model_id, sheet_data)

    model = await get_model_by_id(model_id)
    sheet = await get_revenues_sheet(model_id)

    # merge the data from the integration
    return await merge_accounting_integration_data(
        sheet, str(model.meta.workspace), model.meta.starting_month
    )


@router.get(
    "/model/costs",
    response_model=Sheet,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def retrieve_costs_sheet_of_model(
    model_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve the 'Costs' sheet of a model.\n
        model_id: Model for which to retrieve the sheet
    """
    # model must exist
    await _assert_model_exists(model_id)

    # user must have access to model
    await _assert_access(current_user.id, model_id)

    model = await get_model_by_id(model_id)
    sheet = await get_costs_sheet(model_id)

    # merge the data from the integration
    return await merge_accounting_integration_data(
        sheet, str(model.meta.workspace), model.meta.starting_month
    )


@router.post(
    "/model/costs",
    response_model=Sheet,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def update_costs_sheet_of_model(
    model_id: str,
    sheet_data: Sheet,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update the 'Costs' sheet of a model.\n
        model_id: Model for which to update the sheet
        sheet_data: New data of the sheet
    """
    # model must exist
    await _assert_model_exists(model_id)

    # only editor can update sheet
    await _assert_access_can_edit(current_user.id, model_id)

    assert sheet_data.meta.name == "Costs"

    await update_costs_sheet(model_id, sheet_data)

    model = await get_model_by_id(model_id)
    sheet = await get_costs_sheet(model_id)

    # merge the data from the integration
    return await merge_accounting_integration_data(
        sheet, str(model.meta.workspace), model.meta.starting_month
    )


@router.get(
    "/model/payroll",
    response_model=Payroll,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def retrieve_model_payroll(
    model_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve the payroll information of a model.\n
        model_id: Model for which to retrieve the data
    """
    await _assert_model_exists(model_id)
    await _assert_access(current_user.id, model_id)

    model = await get_model_by_id(model_id)

    # merge the data from the integration
    await merge_payroll_integration_data(
        model.payroll.employees, str(model.meta.workspace), model.meta.starting_month
    )

    from_date = model.meta.starting_month
    to_date = from_date + relativedelta(months=23)

    model.payroll.payroll_values = aggregate_payroll_info(
        model.payroll.employees, model.meta.starting_month, to_date
    )
    return model.payroll


@router.post(
    "/model/payroll",
    response_model=Payroll,
    tags=["model"],
    responses={
        403: {"description": "User does not have access to the resource."},
    },
)
async def update_model_payroll(
    model_id: str,
    employee_data: list[UpdateEmployee],
    current_user: User = Depends(get_current_active_user),
):
    """
    Update the payroll information of a model.\n
        model_id: Model for which to update the payroll
        employee_data: New data of the payroll employees
    """
    await _assert_model_exists(model_id)
    # only editor can update sheet
    await _assert_access_can_edit(current_user.id, model_id)

    # filter out integration data
    filtered = [
        Employee(**employee.dict())
        for employee in employee_data
        if not employee.from_integration
    ]

    await update_model_employees(model_id, filtered)

    # merge the payroll data from the integration
    model = await get_model_by_id(model_id)
    await merge_payroll_integration_data(
        model.payroll.employees, str(model.meta.workspace), model.meta.starting_month
    )

    from_date = model.meta.starting_month
    to_date = from_date + relativedelta(months=23)

    model.payroll.payroll_values = aggregate_payroll_info(
        model.payroll.employees, from_date, to_date
    )
    return model.payroll


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
