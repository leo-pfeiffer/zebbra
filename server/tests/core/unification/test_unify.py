import pytest

from core.unification.unify import parse_value


def test_parse_value_parses_single_word():
    a, b = parse_value("Xero[Hello]")
    assert a == "Xero"
    assert b == "Hello"


def test_parse_value_parses_two_words():
    a, b = parse_value("Xero[Hello World]")
    assert a == "Xero"
    assert b == "Hello World"


def test_parse_value_missing_endpoint():
    with pytest.raises(ValueError):
        parse_value("Xero[]")


def test_parse_value_missing_integration():
    with pytest.raises(ValueError):
        parse_value("[Hello]")


def test_parse_value_space_in_integration():
    with pytest.raises(ValueError):
        parse_value("Xe ro[Hello]")
