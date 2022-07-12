import time
from abc import ABC, abstractmethod

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, Depends, HTTPException
from starlette import status

from api.utils.assertions import assert_workspace_access
from api.utils.dependencies import get_current_active_user_url
from core.dao.integrations import get_integration_for_workspace
from core.schemas.integrations import (
    IntegrationProvider,
    IntegrationAccess,
    IntegrationAccessToken,
)
from core.schemas.users import User
from core.schemas.utils import Message


class IntegrationOAuth(ABC):
    _integration: IntegrationProvider

    @abstractmethod
    def __init__(self):
        self.oauth = OAuth()
        self.oauth_app = None
        self.router = APIRouter()

    def login_url(self):
        return f"/integration/{self.integration().lower()}/login"

    def callback_url(self):
        return f"/integration/{self.integration().lower()}/callback"

    def login_endpoint(self):
        return dict(
            path=f"/integration/{self.integration().lower()}/login",
            tags=["integration"],
            name=f"{self.integration()} OAuth login",
        )

    def callback_endpoint(self):
        return dict(
            path=f"/integration/{self.integration().lower()}/callback",
            tags=["integration"],
            include_in_schema=False,
            name=f"{self.integration()} OAuth callback",
            response_model=Message,
        )

    @classmethod
    @abstractmethod
    def integration(cls):
        raise NotImplementedError("Child class must override method.")

    def register_oauth_app(self, **kwargs):
        self.oauth_app = self.oauth.register(**kwargs)

    @abstractmethod
    async def _perform_token_refresh(
        self, integration_access: IntegrationAccess
    ) -> IntegrationAccess:
        raise NotImplementedError("Child class must override method.")

    @abstractmethod
    async def _store_oauth_token(self, workspace_id, token: IntegrationAccessToken):
        raise NotImplementedError("Child class must override method.")

    # this is the method to be called from the adapter
    async def get_integration_access(self, workspace_id: str) -> IntegrationAccess:
        """
        Retrieve the current integration access data for a workspace for the integration
        :param workspace_id: ID of the workspace
        :return: integration access.
        """
        integration_access = await get_integration_for_workspace(
            workspace_id, self.integration()
        )

        # requires refresh if less than 60 seconds left before expiration
        if integration_access.has_expired():
            integration_access = await self._perform_token_refresh(integration_access)

        return integration_access

    async def oauth_login(
        self,
        workspace_id: str,
        request: Request,
        current_user: User = Depends(get_current_active_user_url),
    ):
        # user must be in workspace
        await assert_workspace_access(current_user.id, workspace_id)

        # !! need to add name=instance.login_url() to routes
        redirect_uri = request.url_for(self.callback_endpoint()["name"])

        # add session info
        request.session["workspace_id"] = workspace_id

        return await self.oauth_app.authorize_redirect(request, redirect_uri)

    async def oauth_callback(self, request: Request):
        token = await self.oauth_app.authorize_access_token(request)

        if token and "workspace_id" in request.session:

            if "expires_at" not in (token_data := {**token}):
                token_data["expires_at"] = token_data["expires_in"] + int(time.time())

            workspace_id = request.session["workspace_id"]

            await self._store_oauth_token(
                workspace_id, IntegrationAccessToken(**token_data)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Connecting to the integration failed.",
            )

        return {"message": "Xero connected. You can close this window."}
