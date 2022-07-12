import datetime

from fastapi import APIRouter, Depends

from api.utils.assertions import (
    assert_workspace_access,
    assert_workspace_has_integration,
    assert_model_access,
)
from api.utils.dependencies import (
    get_current_active_user,
)
from core.dao.integrations import get_integrations_for_workspace
from core.dao.models import get_model_by_id
from core.integrations.adapters.xero_adapter import XeroFetchAdapter
from core.integrations.config import INTEGRATIONS, ADAPTERS
from core.schemas.integrations import (
    IntegrationProviderInfo,
)
from core.schemas.users import User
from core.schemas.utils import DataPoint, DataBatch

router = APIRouter()


# todo this is just for testing and should be removed in production
@router.get("/integration/xero", tags=["integration"], response_model=DataBatch)
async def get_xero_data(
    workspace_id: str,
    from_date: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve all available data from the XERO API for a workspace that is connected
    to the Xero integration\n
        :workspace_id: The id of the workspace whose data to retrieve
        :from_date: The starting date of the date in format YYYY-MM-DD
    """
    # user must be in workspace
    await assert_workspace_access(current_user.id, workspace_id)
    await assert_workspace_has_integration(workspace_id, "Xero")

    from_date = datetime.date.fromisoformat(from_date)
    xfa = XeroFetchAdapter(workspace_id)
    return await xfa.get_data(from_date)


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
    Return all endpoints for all integrations available to a workspace including.\n
        model_id: ID of the workspace
        from_date: Start date of the model
    """

    await assert_model_access(current_user.id, model_id)
    model = await get_model_by_id(model_id)

    data_points = []
    for integration in INTEGRATIONS:
        adapter = ADAPTERS[integration](str(model.meta.workspace))
        points = await adapter.get_data_endpoints(model.meta.starting_month)
        data_points.extend(
            [
                DataPoint(id=f"{integration}[{d}]", integration=integration, name=d)
                for d in points
            ]
        )

    return data_points
