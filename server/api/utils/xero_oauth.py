import time
from base64 import b64encode

from authlib.integrations.starlette_client import OAuth

from core.dao.integrations import (
    get_integration_for_workspace,
    add_integration_for_workspace,
)
from core.schemas.integrations import IntegrationAccessToken, IntegrationAccess

CONF_URL = "https://login.xero.com/identity/.well-known/openid-configuration"
API_URL_SUFFIX = "api.xro/2.0/"
CLIENT_ID = "47CE7326F904481589E07C9073DD5770"
CLIENT_SECRET = "TwnktHFAVllhDM2Pdip1DcBkLVkSZztIAUDfT_LnoAOkq4C0"
REFRESH_URL = "https://identity.xero.com/connect/token"

oauth = OAuth()

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


# todo test
async def perform_token_refresh(integration_access):
    """
    Exchange the current access token with a new token using the OAuth refresh workflow.
    :param integration_access: Current integration access
    :return: Refreshed integration access
    """
    basic_auth = b64encode(str.encode(f"{CLIENT_ID}:{CLIENT_SECRET}")).decode("utf-8")
    token = await xero.post(
        REFRESH_URL,
        withhold_token=True,
        headers={"Authorization": f"Basic {basic_auth}"},
        data={
            "grant_type": "refresh_token",
            "refresh_token": integration_access.token.refresh_token,
        },
    )

    if token.status_code == 200:
        # add expiry information
        token_data = token.json()
        if "expires_at" not in token_data:
            token_data["expires_at"] = token_data["expires_in"] + int(time.time())
        updated_token = IntegrationAccessToken(**token_data)

        # update token in DB
        await store_xero_oauth2_token(integration_access.workspace_id, updated_token)
        integration_access = await get_integration_for_workspace(
            integration_access.workspace_id, "Xero"
        )

    else:
        # todo
        # can't refresh token
        # -> invalidate integration in a way that the user can reconnect and the
        #  references in the data are not lost.
        ...

    return integration_access


# todo test
async def get_xero_integration_access(workspace_id: str) -> IntegrationAccess:
    """
    Retrieve the current integration access data for a workspace for Xero.
    :param workspace_id: ID of the workspace
    :return: integration access.
    """
    integration_access = await get_integration_for_workspace(workspace_id, "Xero")

    # requires refresh if less than 60 seconds left before expiration
    expiry = integration_access.token.expires_at
    now = int(time.time())

    if expiry - 60 < now:
        integration_access = await perform_token_refresh(integration_access)

    return integration_access


# todo test
async def store_xero_oauth2_token(workspace_id, token: IntegrationAccessToken):
    """
    Store Xero integration access for a workspace data in the DB
    :param workspace_id: ID of the workspace
    :param token: OAuth token data
    """
    integration = "Xero"

    tenant_id = await get_xero_tenant_id(workspace_id, token.dict())

    integration_access = IntegrationAccess(
        integration=integration,
        workspace_id=workspace_id,
        token=token,
        tenant_id=tenant_id,
    )

    return await add_integration_for_workspace(integration_access)


# todo test
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
