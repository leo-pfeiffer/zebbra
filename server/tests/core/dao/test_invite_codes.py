import pytest

from core.dao.invite_codes import (
    add_invite_code,
    get_invite_code,
    set_used_by,
    invite_code_exists,
)
from core.schemas.utils import InviteCode
from datetime import datetime, timedelta

from tests.utils import count_documents


@pytest.mark.anyio
async def test_add_invite_code(workspaces):
    token = InviteCode(
        **{
            "invite_code": "somecode",
            "workspace_id": workspaces["ACME Inc."],
            "expires": datetime.utcnow() + timedelta(minutes=100),
            "used_by": None,
        }
    )

    n = await count_documents("invite_codes")
    await add_invite_code(token)
    assert await count_documents("invite_codes") == n + 1


@pytest.mark.anyio
async def test_get_invite_code(workspaces):
    token = InviteCode(
        **{
            "invite_code": "somecode",
            "workspace_id": workspaces["ACME Inc."],
            "expires": datetime.utcnow() + timedelta(minutes=100),
            "used_by": None,
        }
    )

    await add_invite_code(token)
    res = await get_invite_code(token.invite_code)
    assert res.invite_code == token.invite_code


@pytest.mark.anyio
async def test_get_invite_code_no_used_ones(workspaces, users):
    token = InviteCode(
        **{
            "invite_code": "somecode",
            "workspace_id": workspaces["ACME Inc."],
            "expires": datetime.utcnow() + timedelta(minutes=100),
            "used_by": users["alice@example.com"],
        }
    )
    await add_invite_code(token)
    assert await get_invite_code(token.invite_code) is None


@pytest.mark.anyio
async def test_set_used_by(workspaces, users):
    token = InviteCode(
        **{
            "invite_code": "somecode",
            "workspace_id": workspaces["ACME Inc."],
            "expires": datetime.utcnow() + timedelta(minutes=100),
            "used_by": None,
        }
    )

    await add_invite_code(token)
    await set_used_by(token.invite_code, users["alice@example.com"])
    assert await get_invite_code(token.invite_code) is None


@pytest.mark.anyio
async def test_invite_code_exists(workspaces):
    token = InviteCode(
        **{
            "invite_code": "somecode",
            "workspace_id": workspaces["ACME Inc."],
            "expires": datetime.utcnow() + timedelta(minutes=100),
            "used_by": None,
        }
    )

    await add_invite_code(token)
    assert await invite_code_exists(token.invite_code)
