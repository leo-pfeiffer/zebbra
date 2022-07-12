import time
from typing import Literal

from pydantic import BaseModel


# must be of format [A-Za-z\\d]+
IntegrationProvider = Literal["Xero"]


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

    # some integrations might require additional info that can be stored here.
    additional_info: dict | None = None

    def has_expired(self):
        return self.token.expires_at - 60 < int(time.time())
