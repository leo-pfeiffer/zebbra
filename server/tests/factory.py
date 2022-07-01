# test object factory
from core.dao.database import db
import json


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


async def teardown():
    await teardown_users()
    await teardown_workspaces()
    await teardown_token_blacklist()
    await teardown_models()
    await teardown_invite_codes()


def create_user_data():
    return db.users.insert_many(users)


def create_invite_codes_data():
    return db.invite_codes.insert_many(invite_codes)


def create_workspace_data():
    return db.workspaces.insert_many(workspaces)


def create_model_data():
    return db.models.insert_many(models)


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
