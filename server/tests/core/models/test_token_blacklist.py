import pytest

from core.models.token_blacklist import add_to_blacklist, \
    count_blacklisted_tokens, get_blacklisted, is_token_blacklisted
from core.schemas.tokens import Token


@pytest.mark.anyio
async def test_add_to_blacklist():
    token = Token(**{
        "access_token": "mySecureToken",
        "token_type": "password"
    })

    n = await count_blacklisted_tokens()
    await add_to_blacklist(token)
    assert await count_blacklisted_tokens() == n + 1


@pytest.mark.anyio
async def test_get_blacklisted():
    token = Token(**{
        "access_token": "mySecureToken",
        "token_type": "password"
    })

    await add_to_blacklist(token)
    res = await get_blacklisted(token.access_token)
    assert res['access_token'] == token.access_token
    assert res['token_type'] == token.token_type


@pytest.mark.anyio
async def test_is_token_blacklisted():
    token = Token(**{
        "access_token": "mySecureToken",
        "token_type": "password"
    })

    assert not await is_token_blacklisted(token.access_token)
    await add_to_blacklist(token)
    assert await is_token_blacklisted(token.access_token)


@pytest.mark.anyio
async def test_count_blacklisted_tokens():
    token = Token(**{
        "access_token": "mySecureToken",
        "token_type": "password"
    })

    n = await count_blacklisted_tokens()
    assert n == 0
    await add_to_blacklist(token)
    assert await count_blacklisted_tokens() == n + 1

