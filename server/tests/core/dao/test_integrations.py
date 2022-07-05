import pytest

from core.dao.integrations import (
    add_integration_for_workspace,
    get_integrations_for_workspace,
    get_integration_for_workspace,
    workspace_has_integration,
)
from core.schemas.integrations import IntegrationAccess, IntegrationAccessToken
from tests.utils import count_documents


async def setup_integration_access(workspace_id, integration="Xero"):
    await add_integration_for_workspace(
        IntegrationAccess(
            workspace_id=workspace_id,
            integration=integration,
            token=IntegrationAccessToken(
                id_token="id-token",
                access_token="access-token",
                expires_in=1800,
                token_type="Bearer",
                refresh_token="refresh-token",
                scope="some scope",
                expires_at=1656898425,
            ),
            tenant_id="tenant-id",
        )
    )


@pytest.mark.anyio
async def test_get_integrations_for_workspace(workspaces):
    workspace_id = workspaces["ACME Inc."]
    await setup_integration_access(workspace_id, "Xero")
    objs = await get_integrations_for_workspace(workspace_id)
    assert len(objs) == 1
    assert objs[0].workspace_id == workspace_id


@pytest.mark.anyio
async def test_get_integrations_for_workspace_none(workspaces):
    workspace_id1 = workspaces["ACME Inc."]
    workspace_id2 = workspaces["Boring Co."]
    await setup_integration_access(workspace_id1)
    objs = await get_integrations_for_workspace(workspace_id2)
    assert len(objs) == 0


@pytest.mark.anyio
async def test_get_integration_for_workspace(workspaces):
    workspace_id = workspaces["ACME Inc."]
    await setup_integration_access(workspace_id)
    obj = await get_integration_for_workspace(workspace_id, "Xero")
    assert obj.workspace_id == workspace_id


@pytest.mark.anyio
async def test_get_integrations_for_workspace_none(workspaces):
    workspace_id1 = workspaces["ACME Inc."]
    workspace_id2 = workspaces["Boring Co."]
    await setup_integration_access(workspace_id1)
    obj = await get_integration_for_workspace(workspace_id2, "Xero")
    assert obj is None


@pytest.mark.anyio
async def test_workspace_has_integration_true(workspaces):
    workspace_id1 = workspaces["ACME Inc."]
    await setup_integration_access(workspace_id1)
    assert await workspace_has_integration(workspace_id1, "Xero")


@pytest.mark.anyio
async def test_workspace_has_integration_false(workspaces):
    workspace_id1 = workspaces["ACME Inc."]
    workspace_id2 = workspaces["Boring Co."]
    await setup_integration_access(workspace_id1)
    assert not await workspace_has_integration(workspace_id2, "Xero")


@pytest.mark.anyio
async def test_add_integration_for_workspace_new(workspaces):
    workspace_id1 = workspaces["ACME Inc."]
    count_before = await count_documents("integration_access")
    await setup_integration_access(workspace_id1)
    count_after = await count_documents("integration_access")
    assert count_after - count_before == 1


@pytest.mark.anyio
async def test_add_integration_for_workspace_override(workspaces):
    workspace_id1 = workspaces["ACME Inc."]
    count_before = await count_documents("integration_access")
    await setup_integration_access(workspace_id1)
    await setup_integration_access(workspace_id1)
    count_after = await count_documents("integration_access")
    assert count_after - count_before == 1
