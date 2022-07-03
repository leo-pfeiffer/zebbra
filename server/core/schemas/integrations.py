from typing import Literal

from pydantic import BaseModel

from core.objects import PyObjectId


IntegrationProvider = Literal["Xero"]


class IntegrationAccessToken(BaseModel):
    id_token: str
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str
    scope: str
    expires_at: str


class IntegrationAccess(BaseModel):
    user_id: PyObjectId
    integration: IntegrationProvider
    token: IntegrationAccessToken
