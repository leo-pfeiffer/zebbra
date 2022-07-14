import time

import pytest
from dateutil.relativedelta import relativedelta

from core.dao.integrations import get_accounting_cache, set_accounting_cache
from datetime import datetime, timezone

from core.dao.integrations import (
    get_integrations_for_workspace,
    get_integration_for_workspace,
    workspace_has_integration,
    set_requires_reconnect,
)
from core.schemas.utils import DataBatchCache
from tests.factory import setup_integration_access
from tests.utils import count_documents


def compare_rounded_created_at(cached1: DataBatchCache, cached2: DataBatchCache):
    cached1.created_at = cached1.created_at.replace(tzinfo=timezone.utc)
    cached2.created_at = cached2.created_at.replace(tzinfo=timezone.utc)
    return int(cached1.created_at.timestamp()) == int(cached2.created_at.timestamp())


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


@pytest.mark.anyio
async def test_set_requires_reconnect_true(workspaces):
    workspace_id = workspaces["ACME Inc."]
    await set_requires_reconnect(workspace_id, "Xero", True)
    integration_access = await get_integration_for_workspace(workspace_id, "Xero")
    assert integration_access.requires_reconnect


@pytest.mark.anyio
async def test_set_requires_reconnect_false(workspaces):
    workspace_id = workspaces["ACME Inc."]
    await set_requires_reconnect(workspace_id, "Xero", True)
    await set_requires_reconnect(workspace_id, "Xero", False)
    integration_access = await get_integration_for_workspace(workspace_id, "Xero")
    assert not integration_access.requires_reconnect


@pytest.mark.anyio
async def test_set_cached():
    cache_obj = DataBatchCache(
        data={},
        dates=[],
        created_at=datetime.now(tz=timezone.utc),
        workspace_id="123",
        integration="Xero",
        from_date=123,
    )
    await set_accounting_cache(cache_obj)
    db_obj = await get_accounting_cache("123", "Xero", 123)
    assert compare_rounded_created_at(cache_obj, db_obj)


@pytest.mark.anyio
async def test_set_cached_replaces():
    cache_obj = DataBatchCache(
        data={},
        dates=[],
        created_at=datetime.now(tz=timezone.utc),
        workspace_id="123",
        integration="Xero",
        from_date=123,
    )
    await set_accounting_cache(cache_obj)

    cache_obj2 = DataBatchCache(**cache_obj.dict())
    cache_obj2.created_at += relativedelta(minutes=10)
    await set_accounting_cache(cache_obj2)
    time.sleep(1)  # wait for 1 sec to make sure timestamp changes

    db_obj = await get_accounting_cache("123", "Xero", 123)
    assert not compare_rounded_created_at(cache_obj, db_obj)
    assert compare_rounded_created_at(cache_obj2, db_obj)


@pytest.mark.anyio
async def test_get_cached():
    cache_obj = DataBatchCache(
        data={},
        dates=[],
        created_at=datetime.now(tz=timezone.utc),
        workspace_id="123",
        integration="Xero",
        from_date=123,
    )
    await set_accounting_cache(cache_obj)
    db_obj = await get_accounting_cache("123", "Xero", 123)
    assert compare_rounded_created_at(cache_obj, db_obj)


@pytest.mark.anyio
async def test_get_cached_non_existent_from_date():
    cache_obj = DataBatchCache(
        data={},
        dates=[],
        created_at=datetime.now(tz=timezone.utc),
        workspace_id="123",
        integration="Xero",
        from_date=123,
    )
    await set_accounting_cache(cache_obj)
    assert await get_accounting_cache("123", "Xero", 321) is None


@pytest.mark.anyio
async def test_get_cached_non_existent_workspace():
    cache_obj = DataBatchCache(
        data={},
        dates=[],
        created_at=datetime.now(tz=timezone.utc),
        workspace_id="123",
        integration="Xero",
        from_date=123,
    )
    await set_accounting_cache(cache_obj)
    assert await get_accounting_cache("false", "Xero", 123) is None


@pytest.mark.anyio
async def test_get_cached_non_existent_integration():
    cache_obj = DataBatchCache(
        data={},
        dates=[],
        created_at=datetime.now(tz=timezone.utc),
        workspace_id="123",
        integration="Xero",
        from_date=123,
    )
    await set_accounting_cache(cache_obj)
    assert await get_accounting_cache("123", "false", 123) is None  # noqa
