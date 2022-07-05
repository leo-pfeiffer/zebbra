# test object factory
from core.dao.database import db
import json

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

workspaces = _read_json(WORKSPACE_PATH)
users = _read_json(USERS_PATH)
models = _read_json(MODELS_PATH)
invite_codes = _read_json(INVITE_CODES_PATH)


async def create():
    await create_user_data()
    await create_workspace_data()
    await create_model_data()
    await create_invite_codes_data()
    await create_integration_access()


async def teardown():
    await teardown_users()
    await teardown_workspaces()
    await teardown_token_blacklist()
    await teardown_models()
    await teardown_invite_codes()
    await teardown_integration_access()


def create_user_data():
    return db.users.insert_many(users)


def create_invite_codes_data():
    return db.invite_codes.insert_many(invite_codes)


def create_workspace_data():
    return db.workspaces.insert_many(workspaces)


def create_model_data():
    return db.models.insert_many(models)


def create_integration_access():
    return setup_integration_access("62bc5706a40e85213c27ce29")


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
