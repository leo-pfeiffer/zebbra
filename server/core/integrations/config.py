from typing import get_args, Callable

from core.integrations.adapters.adapter import FetchAdapter
from core.integrations.adapters.xero_adapter import XeroFetchAdapter
from core.schemas.integrations import IntegrationProvider


# dynamically created list of integrations from the type
INTEGRATIONS: tuple[IntegrationProvider, ...] = get_args(IntegrationProvider)

ADAPTERS: dict[IntegrationProvider, Callable[[str], FetchAdapter]] = {}


def _register_integration(adapter: FetchAdapter.__class__):
    ADAPTERS[adapter.integration()] = lambda workspace_id: adapter(workspace_id)


def setup_integrations():
    """
    Run on application start to register applications etc.
    """
    _register_integration(XeroFetchAdapter)
