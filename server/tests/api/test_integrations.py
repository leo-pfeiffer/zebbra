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


@pytest.mark.anyio
async def test_integration_providers_all(access_token, workspaces):
    wsp = workspaces["ACME Inc."]
    response = client.get(
        f"/integration/providers?workspace_id={wsp}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

    names = [x["name"] for x in response.json()]

    assert "Gusto" in names
    assert "Xero" in names

    for x in response.json():
        assert x["connected"]


@pytest.mark.anyio
async def test_integration_providers_none(access_token_alice, workspaces):
    wsp = workspaces["Boring Co."]
    response = client.get(
        f"/integration/providers?workspace_id={wsp}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

    for x in response.json():
        assert not x["connected"]


@pytest.mark.anyio
async def test_data_endpoints(access_token):
    model_id = "62b488ba433720870b60ec0a"
    response = client.get(
        f"/integration/dataEndpoints?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    for e in response.json():
        assert e["integration"] == "Xero"


@pytest.mark.anyio
async def test_data_endpoints_no_access(access_token_alice):
    model_id = "62b488ba433720870b60ec0a"
    response = client.get(
        f"/integration/dataEndpoints?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )
    assert response.status_code == 403


@pytest.mark.anyio
async def test_data_endpoints_non_existent_mode(access_token):
    model_id = "not_a_model"
    response = client.get(
        f"/integration/dataEndpoints?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
