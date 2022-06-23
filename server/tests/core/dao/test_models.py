import pytest

from core.dao.models import (
    has_access_to_model,
    get_model_by_id,
    get_models_for_workspace,
    get_models_for_user,
)


@pytest.mark.anyio
async def test_has_access_to_model_admin():
    assert await has_access_to_model("62b488ba433720870b60ec0a", "johndoe@example.com")


@pytest.mark.anyio
async def test_has_access_to_model_editor():
    assert await has_access_to_model("62b488ba433720870b60ec0a", "darwin@example.com")


@pytest.mark.anyio
async def test_has_access_to_model_viewer():
    assert await has_access_to_model("62b488ba433720870b60ec0a", "charlie@example.com")


@pytest.mark.anyio
async def test_has_access_to_model_false():
    assert not await has_access_to_model("62b488ba433720870b60ec0a", "bob@example.com")


@pytest.mark.anyio
async def test_get_model_by_id():
    model_id = "62b488ba433720870b60ec0a"
    models = await get_model_by_id(model_id)
    assert models[0]["_id"] == model_id


@pytest.mark.anyio
async def test_get_model_by_id_no_results():
    model_id = "not_an_id"
    models = await get_model_by_id(model_id)
    assert len(models) == 0


@pytest.mark.anyio
async def test_get_models_for_workspace():
    wsp = "ACME Inc."
    models = await get_models_for_workspace(wsp)
    assert len(models) == 1
    for m in models:
        assert m["meta"]["workspace"] == wsp


@pytest.mark.anyio
async def test_get_models_for_workspace_no_results():
    wsp = "Not a workspace"
    models = await get_models_for_workspace(wsp)
    assert len(models) == 0


@pytest.mark.anyio
async def test_get_models_for_user_admin():
    user = "johndoe@example.com"
    models = await get_models_for_user(user)
    assert len(models) == 1
    for m in models:
        assert m["meta"]["admin"] == user


@pytest.mark.anyio
async def test_get_models_for_user_editor():
    user = "darwin@example.com"
    models = await get_models_for_user(user)
    assert len(models) == 1
    for m in models:
        assert user in m["meta"]["editors"]


@pytest.mark.anyio
async def test_get_models_for_user_viewer():
    user = "charlie@example.com"
    models = await get_models_for_user(user)
    assert len(models) == 1
    for m in models:
        assert user in m["meta"]["viewers"]


@pytest.mark.anyio
async def test_get_models_for_user_no_results():
    user = "not-a-user@example.com"
    models = await get_models_for_user(user)
    assert len(models) == 0
