import datetime
import time

from fastapi import APIRouter, Depends, Request, HTTPException
from starlette import status
from starlette.responses import RedirectResponse, HTMLResponse

from api.utils.assertions import (
    assert_workspace_access,
    assert_workspace_has_integration,
    assert_model_access,
)
from api.utils.dependencies import (
    get_current_active_user_url,
    get_current_active_user,
)
from core.dao.integrations import get_integrations_for_workspace
from core.dao.models import get_model_by_id
from core.schemas.utils import DataPoint, DataBatch
from core.integrations.config import INTEGRATIONS
from core.integrations.adapters.xero_adapter import XeroFetchAdapter
from core.integrations.oauth.xero_oauth import (
    xero,
    store_xero_oauth2_token,
)
from core.schemas.integrations import (
    IntegrationAccessToken,
    IntegrationProviderInfo,
)
from core.schemas.users import User

router = APIRouter()


@router.get("/integration/xero/login", tags=["integration"])
async def integration_xero_login(
    workspace_id: str,
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


@router.get("/integration/xero/callback", tags=["integration"], include_in_schema=False)
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

    return RedirectResponse(url="/integration/connected")


@router.get("/integration/connected", tags=["integration"], include_in_schema=False)
async def integration_xero_done():
    """
    Confirmation page that is called after an integration was connected.
    The page closes the current window.
    """
    html_content = "<script>window.close()</script>"
    return HTMLResponse(content=html_content, status_code=200)


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

    # xero
    xfa = XeroFetchAdapter(str(model.meta.workspace))
    data_points = await xfa.get_data_endpoints(model.meta.starting_month)

    return [DataPoint(id=f"Xero[{d}]", integration="Xero", name=d) for d in data_points]
