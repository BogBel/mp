import pytest
import pytest

@pytest.fixture
def search_not_found_product_html():
    with open(
        "app/tests/crawlers/wollplatz/data/search_not_found_product.html", "r"
    ) as file:
        return file.read()
