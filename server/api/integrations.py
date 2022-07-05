import time

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse, HTMLResponse

from api.utils.assertions import (
    assert_workspace_access,
    assert_workspace_has_integration,
)
from api.utils.dependencies import (
    get_current_active_user_url,
    get_current_active_user,
)
from api.utils.xero_oauth import (
    xero,
    store_xero_oauth2_token,
    get_xero_integration_access,
    API_URL_SUFFIX,
)
from core.schemas.integrations import IntegrationAccessToken
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
    # user must be in workspace
    await assert_workspace_access(current_user.id, workspace_id)

    integration_access = await get_xero_integration_access(workspace_id)
    token = integration_access.token.dict()

    resp = await xero.get("connections", token=token)
    resp.raise_for_status()
    return resp.json()


@router.get("/api/integration/xero/transactions", tags=["integration"])
async def transactions(
    workspace_id: str, current_user: User = Depends(get_current_active_user)
):
    # user must be in workspace
    await assert_workspace_access(current_user.id, workspace_id)
    await assert_workspace_has_integration(workspace_id, "Xero")

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
