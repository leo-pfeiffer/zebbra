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

workspaces = _read_json(WORKSPACE_PATH)
users = _read_json(USERS_PATH)
models = _read_json(MODELS_PATH)


def create_user_data():
    return db.users.insert_many(users)


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
