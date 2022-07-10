# test object factory
from core.dao.database import db
import json
from datetime import datetime, timezone

from core.dao.integrations import add_integration_for_workspace
from core.schemas.integrations import IntegrationAccess, IntegrationAccessToken


def _read_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


USERS_PATH = "resources/demo/users.json"
WORKSPACE_PATH = "resources/demo/workspaces.json"
MODELS_PATH = "resources/demo/models.json"
INVITE_CODES_PATH = "resources/demo/invite_codes.json"
INTEGRATION_ACCESS_PATH = "resources/demo/integration_access.json"
INTEGRATION_CACHE_PATH = "resources/demo/integration_cache.json"

users = _read_json(USERS_PATH)
workspaces = _read_json(WORKSPACE_PATH)
models = _read_json(MODELS_PATH)
invite_codes = _read_json(INVITE_CODES_PATH)
integration_access = _read_json(INTEGRATION_ACCESS_PATH)
integration_cache = _read_json(INTEGRATION_CACHE_PATH)


async def create():
    await create_users()
    await create_workspaces()
    await create_models()
    await create_invite_codes()
    await create_integration_access()
    await create_integration_cache()


async def teardown():
    await teardown_users()
    await teardown_workspaces()
    await teardown_token_blacklist()
    await teardown_models()
    await teardown_invite_codes()
    await teardown_integration_access()
    await teardown_integration_cache()


def create_users():
    return db.users.insert_many(users)


def create_invite_codes():
    return db.invite_codes.insert_many(invite_codes)


def create_workspaces():
    return db.workspaces.insert_many(workspaces)


def create_models():
    return db.models.insert_many(models)


def create_integration_access():
    return db.integration_access.insert_many(integration_access)


def create_integration_cache():
    for element in integration_cache:
        element["created_at"] = datetime.now()
    return db.integration_cache.insert_many(integration_cache)


def teardown_users():
    return db.users.delete_many({})


def teardown_workspaces():
    return db.workspaces.delete_many({})


def teardown_token_blacklist():
    return db.token_blacklist.delete_many({})


def teardown_models():
    return db.models.delete_many({})


def teardown_invite_codes():
    return db.invite_codes.delete_many({})


def teardown_integration_access():
    return db.integration_access.delete_many({})


def teardown_integration_cache():
    return db.integration_cache.delete_many({})


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
