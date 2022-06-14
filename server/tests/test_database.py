import pytest
from core.settings import get_settings


def test_settings_env_is_test():
    settings = get_settings()
    assert settings.dict()['ENV'] == 'test'
    assert settings.dict()['MONGODB_DB'] == 'zebbra_test'
