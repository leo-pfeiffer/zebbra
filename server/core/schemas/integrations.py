import time
from typing import Literal

from pydantic import BaseModel


IntegrationProvider = Literal["Xero"]
supported_providers = ["Xero"]


class IntegrationProviderInfo(BaseModel):
    name: str
    connected: bool
    requires_reconnect: bool


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

    def has_expired(self):
        return self.token.expires_at - 60 < int(time.time())
