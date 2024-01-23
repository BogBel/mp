from typing import Optional

from pydantic import HttpUrl, validator

from app.enums.currency import Currency
from app.models.base_model import Base
from app.utils.convertors import currency_parser


class Price(Base):
    value: float
    currency: str

    @validator("currency", pre=True, allow_reuse=True)
    def parse_currency(cls, v):
        if isinstance(v, Currency):
            return v

        if isinstance(v, str):
            try:
                return Currency[v]
            except KeyError:
                pass
        parsed_currency = currency_parser(v)
        if parsed_currency:
            return parsed_currency
        raise ValueError("Invalid currency")

    @validator("value", pre=True, allow_reuse=True)
    def parse_value(cls, v):
        return cls.convert_to_float(v, "Price.value")


class Product(Base):
    url: HttpUrl
    product_name: str
    brand: str
    price: Price
    availability: bool
