import datetime
import time

from fastapi import APIRouter, Depends, Request, HTTPException
from starlette import status
from starlette.responses import RedirectResponse, HTMLResponse

from api.utils.assertions import (
    assert_workspace_access,
    assert_workspace_has_integration,
)
from api.utils.dependencies import (
    get_current_active_user_url,
    get_current_active_user,
)
from core.dao.integrations import get_integrations_for_workspace
from core.schemas.utils import DataPoint
from core.unification.config import (
    get_supported_providers,
    get_data_point_registry_list,
)
from core.unification.fetch import (
    get_transactions,
    get_tenants,
    get_xero_data_from_data,
    get_available_data_points,
)
from core.unification.xero_oauth import (
    xero,
    store_xero_oauth2_token,
)
from core.schemas.integrations import (
    IntegrationAccessToken,
    IntegrationProviderInfo,
)
from core.schemas.users import User

router = APIRouter()


@router.get("/api/integration/xero/login", tags=["integration"])
async def integration_xero_login(
    workspace_id: str,
    access_token: str,
    request: Request,
    current_user: User = Depends(get_current_active_user_url),
):
    """
    Starting point for the OAuth integration workflow with Xero. Zebbra access token
    (as normally passed to Auth header) must be passed as query parameter
    'access_token' together with the workspace ID
    """

    # user must be in workspace
    await assert_workspace_access(current_user.id, workspace_id)

    redirect_uri = request.url_for("integration_xero_callback")

    # add session info
    request.session["workspace_id"] = workspace_id

    return await xero.authorize_redirect(request, redirect_uri)


@router.get(
    "/api/integration/xero/callback", tags=["integration"], include_in_schema=False
)
async def integration_xero_callback(request: Request):
    """
    OAuth callback for Xero integration.
    """
    token = await xero.authorize_access_token(request)

    if token and "workspace_id" in request.session:

        if "expires_at" not in (token_data := {**token}):
            token_data["expires_at"] = token_data["expires_in"] + int(time.time())

        workspace_id = request.session["workspace_id"]

        await store_xero_oauth2_token(
            workspace_id, IntegrationAccessToken(**token_data)
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Connecting to the integration failed.",
        )

    return RedirectResponse(url="/api/integration/connected")


@router.get("/api/integration/connected", tags=["integration"], include_in_schema=False)
async def integration_xero_done():
    """
    Confirmation page that is called after an integration was connected.
    The page closes the current window.
    """
    html_content = "<script>window.close()</script>"
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/api/integration/xero/tenants", tags=["integration"])
async def tenants(
    workspace_id: str, current_user: User = Depends(get_current_active_user)
):
    # user must be in workspace
    await assert_workspace_access(current_user.id, workspace_id)
    return await get_tenants(workspace_id)


@router.get("/api/integration/xero/transactions", tags=["integration"])
async def transactions(
    workspace_id: str, current_user: User = Depends(get_current_active_user)
):
    # user must be in workspace
    await assert_workspace_access(current_user.id, workspace_id)
    await assert_workspace_has_integration(workspace_id, "Xero")

    return await get_transactions(workspace_id)


@router.get("/api/integration/xero", tags=["integration"])
async def get_xero_data(
    workspace_id: str,
    from_date: str,
    current_user: User = Depends(get_current_active_user),
):
    # user must be in workspace
    await assert_workspace_access(current_user.id, workspace_id)
    await assert_workspace_has_integration(workspace_id, "Xero")

    from_date = datetime.date.fromisoformat(from_date)

    return await get_xero_data_from_data(workspace_id, from_date)


# todo test
@router.get(
    "/api/integration/providers",
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
    workspace_integrations = await get_integrations_for_workspace(workspace_id)
    workspace_integrations_map = {x.integration: x for x in workspace_integrations}

    all_providers = []
    for p in get_supported_providers():
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
    "/api/integration/dataEndpoints",
    tags=["integration"],
    response_model=list[DataPoint],
)
async def data_endpoints(
    workspace_id: str,
    from_date: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Return all endpoints for all integrations available to a workspace including.\n
        :param workspace_id: ID of the workspace
        :param from_date: Start date of the model
        :param current_user: Currently logged-in user
        :return:List of DataPointRegistryEntry
    """

    await assert_workspace_access(current_user.id, workspace_id)

    from_date = datetime.date.fromisoformat(from_date)

    # xero
    data_points = await get_available_data_points(workspace_id, from_date)

    return [DataPoint(id=f"Xero[{d}]", integration="Xero", name=d) for d in data_points]
