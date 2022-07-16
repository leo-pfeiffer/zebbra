import time
from typing import Literal

from pydantic import BaseModel


# must be of format [A-Za-z\\d]+
IntegrationProvider = Literal["Xero", "Gusto"]


class IntegrationProviderInfo(BaseModel):
    name: str
    connected: bool
    requires_reconnect: bool


class IntegrationAccessToken(BaseModel):
    id_token: str | None
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str
    scope: str | None
    expires_at: int


class IntegrationAccess(BaseModel):
    workspace_id: str
    integration: IntegrationProvider
    token: IntegrationAccessToken
    tenant_id: str | None
    requires_reconnect: bool = False

    # some integrations might require additional info that can be stored here.
    additional_info: dict | None = None

    def has_expired(self):
        return self.token.expires_at - 60 < int(time.time())
