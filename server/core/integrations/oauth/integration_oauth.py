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
    """
    Abstract class for OAuth app integration implementation.
    Override this class to build a custom integration using OAuth.
    """

    _integration: IntegrationProvider

    @abstractmethod
    def __init__(self):
        self.oauth = OAuth()
        self.oauth_app = None
        self.router = APIRouter()

    def login_endpoint(self) -> dict:
        """
        Returns a dictionary that is used to generate the login endpoint for the
        OAuth flow.
        Usage:

            @x.router.get(**x.login_endpoint())
            async def login(...):
                ...

        where x is an instance of an implementation of IntegrationOAuth
        """
        return dict(
            path=f"/integration/{self.integration().lower()}/login",
            tags=["integration"],
            name=f"{self.integration()} OAuth login",
        )

    def callback_endpoint(self):
        """
        Returns a dictionary that is used to generate the callback endpoint for the
        OAuth flow.
        Usage:

            @x.router.get(**x.callback_endpoint())
            async def callback(...):
                ...

        where x is an instance of an implementation of IntegrationOAuth
        """
        return dict(
            path=f"/integration/{self.integration().lower()}/callback",
            tags=["integration"],
            include_in_schema=False,
            name=f"{self.integration()} OAuth callback",
            response_model=Message,
        )

    @classmethod
    @abstractmethod
    def integration(cls) -> IntegrationProvider:
        """
        Return the name of the integration. Needs to be implemented by child class
        """
        raise NotImplementedError("Child class must override method.")

    def register_oauth_app(self, **kwargs):
        """
        Register the OAuth app through the authlib starlette client. Kwargs should
        contain all arguments that need to be passed to
        `authlib.integrations.starlette_client.OAuth.register`
        to set up the OAuth app.
        See the authlib documentation for details on what to pass to the method:
        https://docs.authlib.org/en/v0.13/client/frameworks.html#using-oauth-2-0-to-log-in

        After registering, the OAuth app is available as an instance variable as
        IntegrationAccess.oauth_app.
        """
        self.oauth_app = self.oauth.register(**kwargs)

    @abstractmethod
    async def _perform_token_refresh(
        self, integration_access: IntegrationAccess
    ) -> IntegrationAccess:
        """
        This method defines the refresh workflow for an OAuth token refresh for apps
        that have been authenticated before, and which offer a refresh token but whose
        access token has expired.
        The method takes the expired IntegrationAccess object, performs the token
        refresh, updates the IntegrationAccess object with the new tokens and returns
        the updated IntegrationAccess object
        :param integration_access: Current, expired IntegrationAccess object
        :return: Updated IntegrationAccess object with new tokens
        """
        raise NotImplementedError("Child class must override method.")

    @abstractmethod
    async def _store_oauth_token(self, workspace_id, token: IntegrationAccessToken):
        """
        This method stores an oauth token as a IntegrationAccess object in the
        database. This is a relatively simple operation, but can depend on the specific
        OAuth app
        :param workspace_id: Workspace for which to store the access token
        :param token: Access token to store.
        """
        raise NotImplementedError("Child class must override method.")

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
        """
        This method provides the body for a FastAPI route definition to perform
        the login step in the OAuth flow.

        Usage, assuming x is an instance of an implementation of IntegrationOAuth:

            @x.router.get(**x.login_endpoint())
            async def login_route(
                workspace_id: str,
                request: Request,
                current_user: User = Depends(get_current_active_user_url),
            ):
                return await x.oauth_login(workspace_id, request, current_user)

        :param workspace_id: Workspace for which to connect the OAuth app
        :param request: FastAPI request
        :param current_user: Currently logged-in user
        :return: OAuth authorize redirect
        """
        # user must be in workspace
        await assert_workspace_access(current_user.id, workspace_id)

        # !! need to add name=instance.login_url() to routes
        redirect_uri = request.url_for(self.callback_endpoint()["name"])

        # add session info
        request.session["workspace_id"] = workspace_id

        return await self.oauth_app.authorize_redirect(request, redirect_uri)

    async def oauth_callback(self, request: Request):
        """
        This method provides the body for a FastAPI route definition to perform
        the callback step in the OAuth flow.

        Usage, assuming x is an instance of an implementation of IntegrationOAuth:

            @x.router.get(**x.callback_endpoint())
            async def callback_route(request: Request):
                return await x.oauth_callback(request)


        :param request: FastAPI request
        :return: Info message
        """
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
