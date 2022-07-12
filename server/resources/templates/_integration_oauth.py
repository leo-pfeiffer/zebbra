from fastapi import Request, Depends

from api.utils.dependencies import get_current_active_user_url
from core.integrations.oauth.integration_oauth import IntegrationOAuth
from core.schemas.integrations import (
    IntegrationProvider,
    IntegrationAccess,
    IntegrationAccessToken,
)
from core.schemas.users import User


class XxXxXIntegrationOAuth(IntegrationOAuth):
    _integration: IntegrationProvider = "XxXxX"

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
        # todo
        ...

    async def _store_oauth_token(self, workspace_id, token: IntegrationAccessToken):
        """
        Store Xero integration access for a workspace data in the DB
        :param workspace_id: ID of the workspace
        :param token: OAuth token data
        """
        # todo
        ...


XxXxX_integration_oauth = XxXxXIntegrationOAuth()
XxXxX_integration_oauth.register_oauth_app(
    name="XxXxX",
    # todo
)


@XxXxX_integration_oauth.router.get(**XxXxX_integration_oauth.login_endpoint())
async def login_route(
    workspace_id: str,
    request: Request,
    current_user: User = Depends(get_current_active_user_url),
):
    return await XxXxX_integration_oauth.oauth_login(
        workspace_id, request, current_user
    )


@XxXxX_integration_oauth.router.get(**XxXxX_integration_oauth.callback_endpoint())
async def callback_route(request: Request):
    return await XxXxX_integration_oauth.oauth_callback(request)
