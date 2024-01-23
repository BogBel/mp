import pytest

from app.enums.currency import Currency
from app.utils.convertors import currency_parser

def test_valid_currency_symbols():
    assert currency_parser("$") == Currency.USD
    assert currency_parser("€") == Currency.EUR
    assert currency_parser("£") == Currency.GBP

def test_valid_currency_abbreviations():
    assert currency_parser("USD") == Currency.USD
    assert currency_parser("EUR") == Currency.EUR
    assert currency_parser("GBP") == Currency.GBP

def test_invalid_currency_inputs():
    assert currency_parser("invalid") is None
    assert currency_parser("123") is None

def test_case_insensitivity():
    assert currency_parser("usd") == Currency.USD
    assert currency_parser("Eur") == Currency.EUR
    assert currency_parser("gbP") == Currency.GBP

def test_none_input():
    assert currency_parser(None) is None

def test_whitespace_in_input():
    assert currency_parser(" USD ") == Currency.USD
    assert currency_parser("  €  ") == Currency.EUR
    assert currency_parser(" £  ") == Currency.GBP
