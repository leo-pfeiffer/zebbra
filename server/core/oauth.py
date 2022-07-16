from typing import Optional, Dict

from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import HTTPException

from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from urllib.parse import urlparse, parse_qs


class OAuth2PasswordBearerURL(OAuth2):
    """
    Alternative to fastapi.security.OAuth2PasswordBearer where the token
    is passed as a query parameter ['access_token'] instead of in the headers.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:

        # parse the url and its query parameters
        parsed_url = urlparse(str(request.url))
        params = parse_qs(parsed_url.query)

        # if access_token was not provided, raise not authenticated exception
        if "access_token" not in params:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        # return the access token
        return params["access_token"][0]
