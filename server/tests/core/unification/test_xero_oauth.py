import time

import pytest
from fastapi import HTTPException

from core.schemas.integrations import IntegrationAccess, IntegrationAccessToken
from core.unification.xero_oauth import (
    process_refresh_response,
)


class MockResponse:
    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data
        self.text = "Text"

    def json(self):
        return self.data


@pytest.mark.anyio
async def test_process_refresh_response_200(expired_xero_token, workspaces):

    mock_response = MockResponse(
        200,
        dict(
            id_token="new-id-token",
            access_token="new-access-token",
            expires_in=1800,
            token_type="Bearer",
            refresh_token="new-refresh-token",
            scope="some scope",
        ),
    )

    new = await process_refresh_response(mock_response, expired_xero_token)

    # performed update
    assert new.id_token == "new-id-token"

    # added expires at
    assert "expires_at" in new.dict()
    assert new.expires_at >= int(time.time()) + 1799


@pytest.mark.anyio
async def test_process_refresh_response_400(expired_xero_token, workspaces):

    mock_response = MockResponse(
        400,
        dict(
            id_token="new-id-token",
            access_token="new-access-token",
            expires_in=1800,
            token_type="Bearer",
            refresh_token="new-refresh-token",
            scope="some scope",
        ),
    )

    with pytest.raises(HTTPException):
        await process_refresh_response(mock_response, expired_xero_token)


def test_integration_access_has_expired_true(expired_xero_token):
    assert expired_xero_token.has_expired()


def test_integration_access_has_expired_true_in_buffer():
    ia = IntegrationAccess(
        workspace_id="62bc5706a40e85213c27ce29",
        integration="Xero",
        token=IntegrationAccessToken(
            id_token="id-token",
            access_token="access-token",
            expires_in=1800,
            token_type="Bearer",
            refresh_token="refresh-token",
            scope="some scope",
            expires_at=int(time.time()) + 30,
        ),
        tenant_id="tenant-id",
    )

    assert ia.has_expired()


def test_integration_access_has_expired_false(never_expired_xero_token):
    assert not never_expired_xero_token.has_expired()
