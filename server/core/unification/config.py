from core.schemas.integrations import IntegrationProvider
from core.schemas.utils import DataPoint

DATA_POINT_REGISTRY = {
    "Xero": {
        "BankTransactions": {
            "name": "BankTransactions",
            "description": "This endpoint includes spend and receive money transactions, overpayments and prepayments.",
        },
        "Payments": {
            "name": "Payments",
            "description": "Use this method to retrieve either one or many payments for invoices and credit notes",
        },
    }
}


def get_data_point_registry_list(integration: IntegrationProvider):
    return [
        DataPoint(integration=integration, name=v["name"], description=v["description"])
        for k, v in DATA_POINT_REGISTRY[integration].items()
    ]


def get_supported_providers():
    return DATA_POINT_REGISTRY.keys()
