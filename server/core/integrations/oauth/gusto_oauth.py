import time

from fastapi import Request, Depends, HTTPException
from starlette import status

from api.utils.dependencies import get_current_active_user_url
from core.dao.integrations import (
    set_requires_reconnect,
    get_integration_for_workspace,
    add_integration_for_workspace,
)
from core.integrations.oauth.integration_oauth import IntegrationOAuth
from core.logger import logger
from core.schemas.integrations import (
    IntegrationProvider,
    IntegrationAccess,
    IntegrationAccessToken,
)
from core.schemas.users import User
from core.settings import get_settings

settings = get_settings()


class GustoIntegrationOAuth(IntegrationOAuth):
    _integration: IntegrationProvider = "Gusto"

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

        response = await self.oauth_app.post(
            settings.GUSTO_REFRESH_URL,
            withhold_token=True,
            data={
                "client_id": settings.GUSTO_CLIENT_ID,
                "client_secret": settings.GUSTO_CLIENT_SECRET,
                "redirect_uri": "http://localhost:8000/integration/gusto/callback",  # todo try leaving this out
                "refresh_token": integration_access.token.refresh_token,
                "grant_type": "refresh_token",
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
        Store integration access for a workspace data in the DB
        :param workspace_id: ID of the workspace
        :param token: OAuth token data
        """

        tenant_id = await self.get_company(workspace_id, token.dict())

        integration_access = IntegrationAccess(
            integration=self.integration(),
            workspace_id=workspace_id,
            token=token,
            tenant_id=tenant_id,
            requires_reconnect=False,
        )

        return await add_integration_for_workspace(integration_access)

    async def get_company(self, workspace_id, token: dict | None = None):
        """
        Get the first available company ID
        Todo: This is not perfect. If the user has multiple companies, the first one
         is always used
        :param workspace_id: Workspace for which to get the xero data.
        :param token: OAuth token. If not provided, it is retrieved from the DB.
        :return: Tenant ID
        """
        if token is None:
            integration_access = await self.get_integration_access(workspace_id)
            token = integration_access.token.dict()
        if not token:
            return None
        resp = await self.oauth_app.get("v1/me", token={**token})
        resp.raise_for_status()

        data = resp.json()
        if "payroll_admin" in (roles := data["roles"]):
            if "companies" in (payroll_admin := roles["payroll_admin"]):
                if len(payroll_admin["companies"]) != 0:
                    return payroll_admin["companies"][0]["uuid"]

        logger.error("No company found for user in gusto")
        return None


gusto_integration_oauth = GustoIntegrationOAuth()
gusto_integration_oauth.register_oauth_app(
    name="Gusto",
    client_id=settings.GUSTO_CLIENT_ID,
    client_secret=settings.GUSTO_CLIENT_SECRET,
    server_metadata_url=settings.GUSTO_CONF_URL,
    api_base_url=settings.GUSTO_API_BASE_URL,
    authorize_url=settings.GUSTO_AUTHORIZE_URL,
    access_token_url=settings.GUSTO_REFRESH_URL,
)


@gusto_integration_oauth.router.get(**gusto_integration_oauth.login_endpoint())
async def login_route(
    workspace_id: str,
    request: Request,
    current_user: User = Depends(get_current_active_user_url),
):
    return await gusto_integration_oauth.oauth_login(
        workspace_id, request, current_user
    )


@gusto_integration_oauth.router.get(**gusto_integration_oauth.callback_endpoint())
async def callback_route(request: Request):
    return await gusto_integration_oauth.oauth_callback(request)
