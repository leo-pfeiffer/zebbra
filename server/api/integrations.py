from fastapi import APIRouter, Depends, Request

from authlib.integrations.starlette_client import OAuth
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse

from api.utils.assertions import (
    assert_workspace_access,
    assert_workspace_has_integration,
)
from core.dao.integrations import (
    add_integration_for_workspace,
    get_integration_for_workspace,
)
from core.dao.workspaces import get_workspaces_of_user
from core.schemas.integrations import IntegrationAccess, IntegrationAccessToken
from core.schemas.users import User
from api.utils.dependencies import (
    get_current_active_user_url,
    get_current_active_user,
)

router = APIRouter()

oauth = OAuth()

CONF_URL = "https://login.xero.com/identity/.well-known/openid-configuration"
API_URL_SUFFIX = "api.xro/2.0/"
CLIENT_ID = "47CE7326F904481589E07C9073DD5770"
CLIENT_SECRET = "TwnktHFAVllhDM2Pdip1DcBkLVkSZztIAUDfT_LnoAOkq4C0"


xero = oauth.register(
    name="xero",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    api_base_url="https://api.xero.com/",
    client_kwargs={
        "scope": "offline_access openid profile email "
        "accounting.transactions accounting.reports.read "
        "accounting.journals.read accounting.settings "
        "accounting.contacts accounting.attachments "
        "assets projects"
    },
)


async def get_xero_integration_access(workspace_id: str) -> IntegrationAccess:
    return await get_integration_for_workspace(workspace_id, "Xero")


async def store_xero_oauth2_token(workspace_id, token):

    integration = "Xero"

    tenant_id = await get_xero_tenant_id(workspace_id, token)

    integration_access = IntegrationAccess(
        integration=integration,
        workspace_id=workspace_id,
        token=IntegrationAccessToken(**token),
        tenant_id=tenant_id,
    )

    return await add_integration_for_workspace(integration_access)


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

    # user must be in workspace todo
    # await assert_workspace_access(current_user.id, workspace_id)

    redirect_uri = request.url_for("integration_xero_callback")

    # add session info
    request.session["workspace_id"] = workspace_id

    return await oauth.xero.authorize_redirect(request, redirect_uri)


@router.get(
    "/api/integration/xero/callback", tags=["integration"], include_in_schema=False
)
async def integration_xero_callback(request: Request):
    """
    OAuth callback for Xero integration.
    """
    token = await oauth.xero.authorize_access_token(request)

    if token and "workspace_id" in request.session:
        workspace_id = request.session["workspace_id"]
        await store_xero_oauth2_token(workspace_id, token)
    else:
        # todo raise exception
        ...

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

    # user must be in workspace todo
    # await assert_workspace_access(current_user.id, workspace_id)

    integration_access = await get_xero_integration_access(workspace_id)
    token = integration_access.token.dict()

    resp = await xero.get("connections", token=token)
    resp.raise_for_status()
    return resp.json()


@router.get("/api/integration/xero/transactions", tags=["integration"])
async def transactions(
    workspace_id: str, current_user: User = Depends(get_current_active_user)
):

    # user must be in workspace todo
    # await assert_workspace_access(current_user.id, workspace_id)

    integration_access = await get_xero_integration_access(workspace_id)

    resp = await xero.get(
        f"{API_URL_SUFFIX}BankTransactions",
        token=integration_access.token.dict(),
        headers={
            "Xero-Tenant-Id": integration_access.tenant_id,
            "Accept": "application/json",
        },
    )
    resp.raise_for_status()
    return resp.json()


async def get_xero_tenant_id(workspace_id, token: dict | None = None):
    """
    Get the first available tenant ID
    Todo: This is not perfect. If the user has multiple tenants, the first one
     is always used.
    :param workspace_id: Workspace for which to get the xero data.
    :param token: OAuth token. If not provided, it is retreived from the DB.
    :return:
    """
    if token is None:
        integration_access = await get_xero_integration_access(workspace_id)
        token = integration_access.token.dict()
    if not token:
        return None
    resp = await xero.get("connections", token={**token})
    resp.raise_for_status()
    for connection in resp.json():
        if connection["tenantType"] == "ORGANISATION":
            return connection["tenantId"]
