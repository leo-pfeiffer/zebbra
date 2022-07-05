import pytest

from core.dao.integrations import (
    get_integrations_for_workspace,
    get_integration_for_workspace,
    workspace_has_integration,
)
from tests.factory import setup_integration_access
from tests.utils import count_documents


@pytest.mark.anyio
async def test_get_integrations_for_workspace(workspaces):
    workspace_id = workspaces["ACME Inc."]
    objs = await get_integrations_for_workspace(workspace_id)
    assert len(objs) == 1
    assert objs[0].workspace_id == workspace_id


@pytest.mark.anyio
async def test_get_integrations_for_workspace_none(workspaces):
    workspace_id = workspaces["Boring Co."]
    objs = await get_integrations_for_workspace(workspace_id)
    assert len(objs) == 0


@pytest.mark.anyio
async def test_get_integration_for_workspace(workspaces):
    workspace_id = workspaces["ACME Inc."]
    obj = await get_integration_for_workspace(workspace_id, "Xero")
    assert obj.workspace_id == workspace_id


@pytest.mark.anyio
async def test_get_integrations_for_workspace_none(workspaces):
    workspace_id = workspaces["Boring Co."]
    obj = await get_integration_for_workspace(workspace_id, "Xero")
    assert obj is None


@pytest.mark.anyio
async def test_workspace_has_integration_true(workspaces):
    workspace_id = workspaces["ACME Inc."]
    assert await workspace_has_integration(workspace_id, "Xero")


@pytest.mark.anyio
async def test_workspace_has_integration_false(workspaces):
    workspace_id = workspaces["Boring Co."]
    assert not await workspace_has_integration(workspace_id, "Xero")


@pytest.mark.anyio
async def test_add_integration_for_workspace_new(workspaces):
    workspace_id1 = workspaces["Boring Co."]
    count_before = await count_documents("integration_access")
    await setup_integration_access(workspace_id1)
    count_after = await count_documents("integration_access")
    assert count_after - count_before == 1


@pytest.mark.anyio
async def test_add_integration_for_workspace_override(workspaces):
    workspace_id1 = workspaces["ACME Inc."]
    count_before = await count_documents("integration_access")
    await setup_integration_access(workspace_id1)
    count_after = await count_documents("integration_access")
    assert count_after - count_before == 0
