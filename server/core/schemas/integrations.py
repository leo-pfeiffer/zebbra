from typing import Literal

from pydantic import BaseModel


IntegrationProvider = Literal["Xero"]


class IntegrationAccessToken(BaseModel):
    id_token: str
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str
    scope: str
    expires_at: int


class IntegrationAccess(BaseModel):
    workspace_id: str
    integration: IntegrationProvider
    token: IntegrationAccessToken
    tenant_id: str
    requires_reconnect: bool = False
