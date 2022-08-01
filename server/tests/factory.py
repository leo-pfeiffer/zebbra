# test object factory
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from core.dao.database import db
import json
from datetime import datetime

from core.dao.integrations import add_integration_for_workspace
from core.schemas.cache import DataBatchCache, EmployeeListCache
from core.schemas.integrations import IntegrationAccess, IntegrationAccessToken
from core.schemas.models import Model
from core.schemas.users import UserInDB
from core.schemas.utils import DateString, InviteCode
from core.schemas.workspaces import Workspace


def _read_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


DEMO_PATH = "resources/demo/demo.json"
USERS_PATH = "resources/demo/users.json"
WORKSPACE_PATH = "resources/demo/workspaces.json"
MODELS_PATH = "resources/demo/models.json"
INVITE_CODES_PATH = "resources/demo/invite_codes.json"
INTEGRATION_ACCESS_PATH = "resources/demo/integration_access.json"
ACCOUNTING_CACHE_PATH = "resources/demo/accounting_cache.json"
PAYROLL_CACHE_PATH = "resources/demo/payroll_cache.json"

demo = _read_json(DEMO_PATH)
users = _read_json(USERS_PATH)
workspaces = _read_json(WORKSPACE_PATH)
models = _read_json(MODELS_PATH)
invite_codes = _read_json(INVITE_CODES_PATH)
integration_access = _read_json(INTEGRATION_ACCESS_PATH)
accounting_cache = _read_json(ACCOUNTING_CACHE_PATH)
payroll_cache = _read_json(PAYROLL_CACHE_PATH)


async def create():
    await create_demo()
    await create_users()
    await create_workspaces()
    await create_models()
    await create_invite_codes()
    await create_integration_access()
    await create_accounting_cache()
    await create_payroll_cache()


async def teardown():
    await teardown_demo()
    await teardown_users()
    await teardown_workspaces()
    await teardown_token_blacklist()
    await teardown_models()
    await teardown_invite_codes()
    await teardown_integration_access()
    await teardown_accounting_cache()
    await teardown_payroll_cache()


def create_demo():
    return db.demo.insert_many([jsonable_encoder(Model(**e)) for e in demo])


def create_users():
    return db.users.insert_many([jsonable_encoder(UserInDB(**e)) for e in users])


def create_invite_codes():
    return db.invite_codes.insert_many(
        [jsonable_encoder(InviteCode(**e)) for e in invite_codes]
    )


def create_workspaces():
    return db.workspaces.insert_many(
        [jsonable_encoder(Workspace(**e)) for e in workspaces]
    )


def create_models():
    return db.models.insert_many([jsonable_encoder(Model(**e)) for e in models])


def create_integration_access():
    return db.integration_access.insert_many(
        [jsonable_encoder(IntegrationAccess(**e)) for e in integration_access]
    )


def create_accounting_cache():
    for element in accounting_cache:
        element["created_at"] = datetime.now()
    return db.accounting_cache.insert_many(
        [jsonable_encoder(DataBatchCache(**e)) for e in accounting_cache]
    )


def create_payroll_cache():
    for element in payroll_cache:
        element["created_at"] = datetime.now()
    return db.payroll_cache.insert_many(
        [jsonable_encoder(EmployeeListCache(**e)) for e in payroll_cache]
    )


def teardown_demo():
    return db.demo.delete_many({})


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


def teardown_accounting_cache():
    return db.accounting_cache.delete_many({})


def teardown_payroll_cache():
    return db.payroll_cache.delete_many({})


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


class FakeEmployee(BaseModel):
    start_date: DateString
    end_date: DateString | None
    monthly_salary: int
