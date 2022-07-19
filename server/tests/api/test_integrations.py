import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.anyio
async def test_disconnect_integration(access_token, workspaces):
    wsp = workspaces["ACME Inc."]
    response = client.post(
        f"/integration/disconnect?workspace_id={wsp}&integration=Xero",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Integration Xero has been disconnected"


@pytest.mark.anyio
async def test_disconnect_integration_not_connected(access_token_alice, workspaces):
    wsp = workspaces["Boring Co."]
    response = client.post(
        f"/integration/disconnect?workspace_id={wsp}&integration=Xero",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Integration Xero is not connected"
