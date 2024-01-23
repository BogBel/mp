from pydantic import validator
from app.models.base_model import Base


class QueryProduct(Base):
    id: int
    brand_name: str
    product_name: str

    @validator("product_name", pre=True, allow_reuse=True)
    def check_string_not_empty(cls, v):
        if not isinstance(v, str) or len(v.strip()) == 0:
            raise ValueError(" name must be a non-empty string")
        return v
