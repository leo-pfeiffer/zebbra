import time
from base64 import b64encode
from fastapi import HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette import status

from core.dao.integrations import (
    get_integration_for_workspace,
    add_integration_for_workspace,
    set_requires_reconnect,
)
from core.logger import logger
from core.schemas.integrations import IntegrationAccessToken, IntegrationAccess
from core.settings import get_settings

settings = get_settings()

CLIENT_ID = settings.XERO_CLIENT_ID
CLIENT_SECRET = settings.XERO_CLIENT_SECRET
CONF_URL = settings.XERO_CONF_URL
API_BASE_URL = settings.XERO_API_BASE_URL
API_URL_SUFFIX = settings.XERO_API_URL_SUFFIX
REFRESH_URL = settings.XERO_REFRESH_URL

oauth = OAuth()

xero = oauth.register(
    name="xero",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    api_base_url=API_BASE_URL,
    client_kwargs={
        "scope": "offline_access openid profile email "
        "accounting.transactions accounting.reports.read "
        "accounting.journals.read accounting.settings "
        "accounting.contacts accounting.attachments "
        "assets projects"
    },
)


async def perform_token_refresh(integration_access):
    """
    Exchange the current access token with a new token using the OAuth refresh workflow
    :param integration_access: Current integration access
    :return: Refreshed integration access
    """

    logger.info(
        f"Refreshing token for "
        f"{integration_access.workspace_id} : {integration_access.integration}"
    )

    basic_auth = b64encode(str.encode(f"{CLIENT_ID}:{CLIENT_SECRET}")).decode("utf-8")
    response = await xero.post(
        REFRESH_URL,
        withhold_token=True,
        headers={"Authorization": f"Basic {basic_auth}"},
        data={
            "grant_type": "refresh_token",
            "refresh_token": integration_access.token.refresh_token,
        },
    )

    token = await process_refresh_response(response, integration_access)
    # update token in DB
    await store_xero_oauth2_token(integration_access.workspace_id, token)
    return await get_integration_for_workspace(integration_access.workspace_id, "Xero")


async def process_refresh_response(
    response, integration_access: IntegrationAccess
) -> IntegrationAccessToken:
    """
    Process the response from the POST request to refresh the OAuth token
    :param response: Response to the refresh request
    :param integration_access: integration access data
    :return: Refreshed token
    """
    if response.status_code == 200:
        # add expiry information
        token_data = response.json()
        if "expires_at" not in token_data:
            token_data["expires_at"] = token_data["expires_in"] + int(time.time())
        return IntegrationAccessToken(**token_data)

    # Can't refresh token -> set the requires_reconnect value of the integration
    #  access to True, indicating that the user has to go through the OAuth
    #  connection workflow to reconnect the integration. The integration access ID
    #  remains the same.
    await set_requires_reconnect(integration_access.workspace_id, "Xero", True)

    logger.error(
        f"Token refresh failed. Response: {response.status_code}, {response.text}"
    )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token refresh failed.",
    )


async def get_xero_integration_access(workspace_id: str) -> IntegrationAccess:
    """
    Retrieve the current integration access data for a workspace for Xero
    :param workspace_id: ID of the workspace
    :return: integration access.
    """
    integration_access = await get_integration_for_workspace(workspace_id, "Xero")

    # requires refresh if less than 60 seconds left before expiration
    if integration_access.has_expired():
        integration_access = await perform_token_refresh(integration_access)

    return integration_access


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
        requires_reconnect=False,
    )

    return await add_integration_for_workspace(integration_access)


async def get_xero_tenant_id(workspace_id, token: dict | None = None):
    """
    Get the first available tenant ID
    Todo: This is not perfect. If the user has multiple tenants, the first one
     is always used.
    :param workspace_id: Workspace for which to get the xero data.
    :param token: OAuth token. If not provided, it is retrieved from the DB.
    :return: Tenant ID
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
