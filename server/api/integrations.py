from fastapi import APIRouter, Depends, Request

from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse, HTMLResponse

from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
import json

from api.utils.assertions import assert_workspace_access
from core.dao.integrations import (
    add_integration_for_workspace,
    get_integration_for_workspace,
)
from core.dao.workspaces import get_workspaces_of_user
from core.schemas.integrations import IntegrationAccess, IntegrationAccessToken
from core.schemas.users import User
from api.utils.dependencies import (
    get_current_active_user_url,
)

router = APIRouter()

oauth = OAuth()

CONF_URL = "https://login.xero.com/identity/.well-known/openid-configuration"
CLIENT_ID = "47CE7326F904481589E07C9073DD5770"
CLIENT_SECRET = "TwnktHFAVllhDM2Pdip1DcBkLVkSZztIAUDfT_LnoAOkq4C0"


xero = oauth.register(
    name="xero",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "offline_access openid profile email "
        "accounting.transactions accounting.reports.read "
        "accounting.journals.read accounting.settings "
        "accounting.contacts accounting.attachments "
        "assets projects"
    },
)

api_client = ApiClient(
    Configuration(
        debug=True,
        oauth2_token=OAuth2Token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET),
    ),
    pool_threads=1,
)


@api_client.oauth2_token_getter
async def obtain_xero_oauth2_token(workspace_id: str):
    integration_access = await get_integration_for_workspace(workspace_id, "Xero")
    return integration_access.token


@api_client.oauth2_token_saver
async def store_xero_oauth2_token(token, workspace_id):

    integration = "Xero"

    integration_access = IntegrationAccess(
        integration=integration,
        workspace_id=workspace_id,
        token=IntegrationAccessToken(**token),
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

    # user must be in workspace
    await assert_workspace_access(current_user.id, workspace_id)

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

    workspace_id = request.session["workspace_id"]

    if token and "workspace_id" in request.session:
        await store_xero_oauth2_token(token, workspace_id)
    else:
        # todo raise exception
        ...

    # user = token.get("userinfo")
    # if user:
    #     request.session["user"] = user

    # do something with the token
    return RedirectResponse(url="/api/integration/connected")


@router.get("/api/integration/connected", tags=["integration"], include_in_schema=False)
async def integration_xero_done():
    """
    Confirmation page that is called after an integration was connected.
    The page closes the current window.
    """
    html_content = "<script>window.close()</script>"
    return HTMLResponse(content=html_content, status_code=200)
