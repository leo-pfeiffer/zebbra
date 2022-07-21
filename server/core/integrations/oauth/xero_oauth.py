import time
from base64 import b64encode

from fastapi import Depends, Request
from fastapi import HTTPException
from starlette import status

from api.utils.dependencies import get_current_active_user_url
from core.dao.integrations import (
    get_integration_for_workspace,
    add_integration_for_workspace,
    set_requires_reconnect,
)
from core.integrations.oauth.integration_oauth import IntegrationOAuth
from core.logger import logger
from core.schemas.integrations import (
    IntegrationAccessToken,
    IntegrationAccess,
    IntegrationProvider,
)
from core.schemas.users import User
from core.settings import get_settings

settings = get_settings()

CLIENT_ID = settings.XERO_CLIENT_ID
CLIENT_SECRET = settings.XERO_CLIENT_SECRET
CONF_URL = settings.XERO_CONF_URL
API_BASE_URL = settings.XERO_API_BASE_URL
API_URL_SUFFIX = settings.XERO_API_URL_SUFFIX
REFRESH_URL = settings.XERO_REFRESH_URL


class XeroIntegrationOAuth(IntegrationOAuth):

    _integration: IntegrationProvider = "Xero"

    def __init__(self):
        super().__init__()

    @classmethod
    def integration(cls):
        return cls._integration

    async def _perform_token_refresh(self, integration_access: IntegrationAccess):
        """
        Exchange the current access token with a new token using the OAuth refresh workflow
        :param integration_access: Current integration access
        :return: Refreshed integration access
        """

        logger.info(
            f"Refreshing token for "
            f"{integration_access.workspace_id} : {integration_access.integration}"
        )

        basic_auth = b64encode(str.encode(f"{CLIENT_ID}:{CLIENT_SECRET}")).decode(
            "utf-8"
        )
        response = await self.oauth_app.post(
            REFRESH_URL,
            withhold_token=True,
            headers={"Authorization": f"Basic {basic_auth}"},
            data={
                "grant_type": "refresh_token",
                "refresh_token": integration_access.token.refresh_token,
            },
        )

        token = await self._process_refresh_response(response, integration_access)

        # update token in DB
        await self._store_oauth_token(integration_access.workspace_id, token)
        return await get_integration_for_workspace(
            integration_access.workspace_id, self.integration()
        )

    async def _process_refresh_response(
        self, response, integration_access: IntegrationAccess
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
        await set_requires_reconnect(
            integration_access.workspace_id, self.integration(), True
        )

        logger.error(
            f"Token refresh failed. Response: {response.status_code}, {response.text}"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token refresh failed.",
        )

    async def _store_oauth_token(self, workspace_id, token: IntegrationAccessToken):
        """
        Store Xero integration access for a workspace data in the DB
        :param workspace_id: ID of the workspace
        :param token: OAuth token data
        """
        tenant_id = await self.get_xero_tenant_id(workspace_id, token.dict())

        integration_access = IntegrationAccess(
            integration=self.integration(),
            workspace_id=workspace_id,
            token=token,
            tenant_id=tenant_id,
            requires_reconnect=False,
        )

        return await add_integration_for_workspace(integration_access)

    async def get_xero_tenant_id(self, workspace_id, token: dict | None = None):
        """
        Get the first available tenant ID.
        Note that if the user has multiple tenants, the first one is always used
        :param workspace_id: Workspace for which to get the xero data
        :param token: OAuth token. If not provided, it is retrieved from the DB
        :return: Tenant ID
        """
        if token is None:
            integration_access = await self.get_integration_access(workspace_id)
            token = integration_access.token.dict()
        if not token:
            return None
        resp = await self.oauth_app.get("connections", token={**token})
        resp.raise_for_status()
        for connection in resp.json():
            if connection["tenantType"] == "ORGANISATION":
                return connection["tenantId"]


xero_integration_oauth = XeroIntegrationOAuth()
xero_integration_oauth.register_oauth_app(
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


@xero_integration_oauth.router.get(**xero_integration_oauth.login_endpoint())
async def integration_xero_login(
    workspace_id: str,
    request: Request,
    current_user: User = Depends(get_current_active_user_url),
):
    return await xero_integration_oauth.oauth_login(workspace_id, request, current_user)


@xero_integration_oauth.router.get(**xero_integration_oauth.callback_endpoint())
async def integration_xero_callback(request: Request):
    return await xero_integration_oauth.oauth_callback(request)
