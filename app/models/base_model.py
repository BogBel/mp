from pydantic import BaseModel


class Base(BaseModel):
    @classmethod
    def validate_string_not_empty(cls, value, field_name):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} must be a non-empty string")
        return value

    @classmethod
    def convert_to_float(cls, value, field_name):
        if isinstance(value, str):
            value = value.replace(",", ".")
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} Can't convert {value} to float")
