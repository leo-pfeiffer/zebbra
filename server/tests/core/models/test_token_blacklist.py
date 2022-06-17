import pytest

from core.models.token_blacklist import add_to_blacklist, \
    count_blacklisted_tokens, get_blacklisted, is_token_blacklisted
from core.schemas.tokens import BlacklistToken


@pytest.mark.anyio
async def test_add_to_blacklist():
    token = BlacklistToken(**{
        "access_token": "mySecureToken",
    })

    n = await count_blacklisted_tokens()
    await add_to_blacklist(token)
    assert await count_blacklisted_tokens() == n + 1


@pytest.mark.anyio
async def test_get_blacklisted():
    token = BlacklistToken(**{
        "access_token": "mySecureToken",
    })

    await add_to_blacklist(token)
    res = await get_blacklisted(token.access_token)
    assert res['access_token'] == token.access_token


@pytest.mark.anyio
async def test_is_token_blacklisted():
    token = BlacklistToken(**{
        "access_token": "mySecureToken",
    })

    assert not await is_token_blacklisted(token.access_token)
    await add_to_blacklist(token)
    assert await is_token_blacklisted(token.access_token)


@pytest.mark.anyio
async def test_count_blacklisted_tokens():
    token = BlacklistToken(**{
        "access_token": "mySecureToken",
    })

    n = await count_blacklisted_tokens()
    assert n == 0
    await add_to_blacklist(token)
    assert await count_blacklisted_tokens() == n + 1
