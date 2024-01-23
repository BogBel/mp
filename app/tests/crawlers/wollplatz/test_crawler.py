import pytest
from unittest.mock import AsyncMock

from app.crawlers.wollplatz.crawler import Wollplatz
from app.models.query_product import QueryProduct
from app.models.response import Response


@pytest.mark.asyncio
async def test_wollplatz_search_not_found_results(search_not_found_product_html):
    crawler = Wollplatz()

    # Mock the perform_request method
    response = Response(
        status_code=200, headers={}, cookies={}, text=search_not_found_product_html
    )
    crawler.perform_request = AsyncMock(return_value=response)

    # Using dummy query product.
    query_product = QueryProduct(id=1, brand_name="Brand", product_name="Product")

    result = await crawler.search(query_product)

    # TODO assert that the perform_request method was called with the correct arguments
    assert result is None


@pytest.mark.asyncio
async def test_wollplatz_search_found_results(search_found_product_html):
    crawler = Wollplatz()

    # Mock the perform_request method
    response = Response(
        status_code=200, headers={}, cookies={}, text=search_found_product_html
    )
    crawler.perform_request = AsyncMock(return_value=response)

    # Using dummy query product.
    query_product = QueryProduct(id=1, brand_name="Brand", product_name="Product")

    result = await crawler.search(query_product)

    # TODO assert that the perform_request method was called with the correct arguments
    assert result is None
