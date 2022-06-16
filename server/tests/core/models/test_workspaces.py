import pytest

from core.exceptions import UniqueConstraintFailedException
from core.models.users import get_user, delete_user, add_user_to_workspace
from core.models.workspaces import get_workspaces_of_user, create_workspace, \
    get_workspace
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
    new_wsp = Workspace(**{
        "name": "New Workspace",
        "admin": "johndoe@example.com",
        "users": ["johndoe@example.com"]
    })

    await create_workspace(new_wsp)
    wsp = await get_workspace("New Workspace")
    assert wsp is not None


@pytest.mark.anyio
async def test_cannot_create_workspace_with_duplicate_name():
    new_wsp = Workspace(**{
        "name": "ACME Inc.",
        "admin": "johndoe@example.com",
        "users": ["johndoe@example.com"]
    })

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