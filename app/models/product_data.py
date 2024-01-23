from app.models.base_model import Base
from app.models.query_product import QueryProduct
from app.models.product import Product


class ProductData(Base):
    query_data: QueryProduct
    products: list[Product] = []
