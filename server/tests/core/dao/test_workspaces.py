import pytest

from core.dao.models import get_models_for_workspace, add_admin_to_model
from core.dao.users import add_user_to_workspace
from core.dao.workspaces import (
    get_workspaces_of_user,
    create_workspace,
    get_workspace,
    get_admin_workspaces_of_user,
    change_workspace_admin,
    is_user_in_workspace,
    change_workspace_name,
    is_user_admin_of_workspace,
    get_users_of_workspace,
)
from core.exceptions import UniqueConstraintFailedException, DoesNotExistException
from core.schemas.workspaces import Workspace


@pytest.mark.anyio
async def test_get_workspace_returns_workspace():
    name = "Boring Co."
    wsp = await get_workspace(name)
    assert wsp.name == name


@pytest.mark.anyio
async def test_get_non_existing_workspace_returns_none():
    name = "Not a workspace"
    wsp = await get_workspace(name)
    assert wsp is None


@pytest.mark.anyio
async def test_create_workspace():
    new_wsp = Workspace(
        **{
            "name": "New Workspace",
            "admin": "johndoe@example.com",
            "users": ["johndoe@example.com"],
        }
    )

    await create_workspace(new_wsp)
    wsp = await get_workspace("New Workspace")
    assert wsp is not None


@pytest.mark.anyio
async def test_cannot_create_workspace_with_duplicate_name():
    new_wsp = Workspace(
        **{
            "name": "ACME Inc.",
            "admin": "johndoe@example.com",
            "users": ["johndoe@example.com"],
        }
    )

    with pytest.raises(UniqueConstraintFailedException):
        await create_workspace(new_wsp)


@pytest.mark.anyio
async def test_get_workspaces_of_user():
    username = "johndoe@example.com"
    await add_user_to_workspace(username, "Boring Co.")
    wsps = [w.name for w in await get_workspaces_of_user(username)]

    assert len(wsps) == 2
    assert "Boring Co." in wsps
    assert "ACME Inc." in wsps


@pytest.mark.anyio
async def test_get_admin_workspaces_of_user():
    username = "johndoe@example.com"
    await add_user_to_workspace(username, "Boring Co.")
    wsps = [w.name for w in await get_admin_workspaces_of_user(username)]

    assert len(wsps) == 1
    assert "ACME Inc." in wsps


@pytest.mark.anyio
async def test_user_in_workspace():
    username = "johndoe@example.com"
    workspace = "ACME Inc."
    assert await is_user_in_workspace(username, workspace)


@pytest.mark.anyio
async def test_user_not_in_workspace():
    username = "johndoe@example.com"
    workspace = "Boring Co."
    assert not await is_user_in_workspace(username, workspace)


@pytest.mark.anyio
async def test_change_workspace_admin():
    wsp = "Boring Co."
    username = "johndoe@example.com"
    await change_workspace_admin(wsp, username)

    updated = await get_workspace(wsp)
    assert updated.admin == username


@pytest.mark.anyio
async def test_change_workspace_admin_updates_model_admins():
    wsp = "ACME Inc."
    username = "charlie@example.com"
    await change_workspace_admin(wsp, username)

    updated = await get_workspace(wsp)
    assert updated.admin == username

    models = await get_models_for_workspace(wsp)
    for m in models:
        assert username in m["meta"]["admins"]


@pytest.mark.anyio
async def test_change_workspace_admin_updates_model_admins_no_duplicates():
    wsp = "ACME Inc."
    username = "charlie@example.com"

    models = await get_models_for_workspace(wsp)
    for m in models:
        await add_admin_to_model(username, m["_id"])

    await change_workspace_admin(wsp, username)

    updated = await get_workspace(wsp)
    assert updated.admin == username

    models = await get_models_for_workspace(wsp)
    for m in models:
        assert len([x for x in m["meta"]["admins"] if x == username]) == 1


@pytest.mark.anyio
async def test_cannot_change_workspace_admin_to_non_existing_user():
    wsp = "Boring Co."
    username = "notauser@example.com"

    with pytest.raises(DoesNotExistException):
        await change_workspace_admin(wsp, username)


@pytest.mark.anyio
async def test_change_workspace_name():
    wsp = "Boring Co."
    new_name = "Tesla Co."

    await change_workspace_name(wsp, new_name)
    assert await get_workspace(wsp) is None
    assert await get_workspace(new_name) is not None


@pytest.mark.anyio
async def test_change_workspace_name_duplicate():
    wsp = "Boring Co."
    new_name = "ACME Inc."

    with pytest.raises(UniqueConstraintFailedException):
        await change_workspace_name(wsp, new_name)


@pytest.mark.anyio
async def test_user_is_admin():
    username = "johndoe@example.com"
    workspace = "ACME Inc."
    assert await is_user_admin_of_workspace(username, workspace)


@pytest.mark.anyio
async def test_user_is_admin_false():
    username = "alice@example.com"
    workspace = "ACME Inc."
    assert not await is_user_admin_of_workspace(username, workspace)


@pytest.mark.anyio
async def test_get_users_of_workspace(access_token):
    users = await get_users_of_workspace("ACME Inc.")
    unique = set()
    wsp = await get_workspace("ACME Inc.")
    wsp_users = set(wsp.users)
    wsp_users.add(wsp.admin)

    for u in users:
        if u.username == "johndoe@example.com":
            assert u.user_role == "Admin"
        else:
            assert u.user_role == "Member"
        unique.add(u.username)

        assert u.username in wsp_users

    assert len(users) == len(unique)
    assert len(wsp_users) == len(unique)


@pytest.mark.anyio
async def test_get_users_of_workspace_workspace_non_existent(access_token):
    with pytest.raises(DoesNotExistException):
        await get_users_of_workspace("Not a workspace.")
