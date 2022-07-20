import datetime

from fastapi import APIRouter, Depends

from api.utils.assertions import (
    assert_workspace_access,
    assert_model_access,
    assert_workspace_access_admin,
)
from api.utils.dependencies import (
    get_current_active_user,
)
from core.dao.integrations import (
    get_integrations_for_workspace,
    workspace_has_integration,
    remove_integration_for_workspace,
)
from core.dao.models import get_model_by_id
from core.integrations.config import INTEGRATIONS, ADAPTERS
from core.schemas.integrations import (
    IntegrationProviderInfo,
    IntegrationProvider,
)
from core.schemas.users import User
from core.schemas.utils import DataPoint, Message

router = APIRouter()


@router.post("/integration/disconnect", tags=["integration"], response_model=Message)
async def disconnect_integration(
    workspace_id: str,
    integration: IntegrationProvider,
    current_user: User = Depends(get_current_active_user),
):
    await assert_workspace_access_admin(current_user.id, workspace_id)

    if not await workspace_has_integration(workspace_id, integration):
        return {"message": f"Integration {integration} is not connected"}
    else:
        await remove_integration_for_workspace(workspace_id, integration)
        return {"message": f"Integration {integration} has been disconnected"}


# todo test
@router.get(
    "/integration/providers",
    tags=["integration"],
    response_model=list[IntegrationProviderInfo],
)
async def providers(
    workspace_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Return all integration providers for a workspace including information if the
    integration is connected.\n
        :param workspace_id: ID of the workspace
        :param current_user: Currently logged-in user
        :return:List of IntegrationProviderInfo
    """

    await assert_workspace_access(current_user.id, workspace_id)

    workspace_integrations = await get_integrations_for_workspace(workspace_id)
    workspace_integrations_map = {x.integration: x for x in workspace_integrations}

    all_providers = []
    for p in INTEGRATIONS:
        if p in workspace_integrations_map:
            info = IntegrationProviderInfo(
                name=p,
                connected=True,
                requires_reconnect=workspace_integrations_map[p].requires_reconnect,
            )
        else:
            info = IntegrationProviderInfo(
                name=p, connected=False, requires_reconnect=False
            )
        all_providers.append(info)

    return all_providers


# todo test
@router.get(
    "/integration/dataEndpoints",
    tags=["integration"],
    response_model=list[DataPoint],
)
async def data_endpoints(
    model_id: str,  # use model_id instead
    current_user: User = Depends(get_current_active_user),
):
    """
    Return all endpoints for all integrations available to a workspace.\n
        model_id: ID of the workspace
        from_date: Start date of the model
    """

    await assert_model_access(current_user.id, model_id)
    model = await get_model_by_id(model_id)

    data_points = []
    for integration in INTEGRATIONS:
        adapter = ADAPTERS[integration](str(model.meta.workspace))

        # payroll adapters have no endpoints
        if adapter.api_type() == "payroll":
            continue

        points = await adapter.get_data_endpoints(model.meta.starting_month)
        data_points.extend(
            [
                DataPoint(id=f"{integration}[{d}]", integration=integration, name=d)
                for d in points
            ]
        )

    return data_points
