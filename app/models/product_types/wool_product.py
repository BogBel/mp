from typing import Optional

from app.models.product import Product


class WoolProduct(Product):
    needle_size: Optional[str]  # Optional since not all wool products may specify this
    composition: Optional[str]  # Optional for the same reason
