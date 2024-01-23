from typing import Union

from app.enums.currency import Currency


def currency_parser(val: Union[str, None]) -> str:
    if not val:
        return None
    currency_map = {
        "€": Currency.EUR,
        "euro": Currency.EUR,
        "EUR": Currency.EUR,
        "GBP": Currency.GBP,
        "£": Currency.GBP,
        "USD": Currency.USD,
        "$": Currency.USD,
    }
    val = val.strip().lower()
    return currency_map.get(val, None)
