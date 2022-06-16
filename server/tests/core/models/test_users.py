import pytest

from core.exceptions import UniqueConstraintFailedException
from core.models.users import get_user, delete_user, add_user_to_workspace, \
    create_user
from core.models.workspaces import get_workspaces_of_user, create_workspace, \
    get_workspace
from core.schemas.users import UserInDB


@pytest.mark.anyio
async def test_create_user():
    new_user = UserInDB(**{
        "username": "another@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "workspaces": ["ACME Inc."],
        "email": "another@example.com",
        "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
        "disabled": False
    })
    await create_user(new_user)
    user = await get_user("another@example.com")
    assert user is not None


@pytest.mark.anyio
async def test_cannot_create_user_with_duplicate_username():
    new_user = UserInDB(**{
        "username": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "workspaces": ["ACME Inc."],
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
        "disabled": False
    })
    with pytest.raises(UniqueConstraintFailedException):
        await create_user(new_user)


@pytest.mark.anyio
async def test_get_user_returns_user():
    user = await get_user("johndoe@example.com")
    assert user.username == "johndoe@example.com"


@pytest.mark.anyio
async def test_get_non_existing_user_returns_none():
    user = await get_user("notauser@me.com")
    assert user is None


@pytest.mark.anyio
async def test_delete_user_deletes_user():
    await delete_user("johndoe@example.com")
    assert await get_user("johndoe@example.com") is None


@pytest.mark.anyio
async def test_delete_user_deletes_workspace_membership():
    assert len(await get_workspaces_of_user("johndoe@example.com")) == 1
    await delete_user("johndoe@example.com")
    assert len(await get_workspaces_of_user("johndoe@example.com")) == 0


@pytest.mark.anyio
async def test_add_user_to_workspace():
    wsp = "Boring Co."
    username = "johndoe@example.com"
    await add_user_to_workspace(username, wsp)
    user = await get_user(username)
    assert len(user.workspaces) == 2
    assert wsp in user.workspaces
    workspace = await get_workspace(wsp)
    assert len(workspace.users) == 2
    assert username in workspace.users

