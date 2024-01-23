import time
from typing import Union

from app.crawlers.base_crawler import BaseCrawler
from app.crawlers.wollplatz.constants import (
    ProductPaths,
    RequestData,
    SearchPaths,
)
from app.enums.crawler_name import CrawlerName
from app.models.product import Price
from app.models.product_types.wool_product import WoolProduct
from app.models.query_product import QueryProduct


class Wollplatz(BaseCrawler):
    name = CrawlerName.WOLLPLATZ

    async def search(self, search_query: QueryProduct) -> Union[str, None]:
        """Search for a product on the Wollplatz website"""
        query = f"{search_query.brand_name} {search_query.product_name}"
        params = dict(
            **{"searchQuery": query, "_": int(time.time() * 1000)},
            **RequestData.search_params,
        )
        search_page_response = await self.perform_request(
            RequestData.search_url, params=params, headers=RequestData.headers
        )
        with open("search_found.html", "w") as file:
            file.write(search_page_response.text)
        left_split = search_page_response.text.split(
            "sendSearchQueryByScriptCompleted(", 1
        )[1]
        json_part = left_split.rsplit(");", 1)[0]
        json_data = self.build_json(json_part)
        if not all(
            (
                json_data.get("resultsPanel", {}).get("numberOfResults"),
                json_data.get("resultsPanel", {}).get("html"),
            )
        ):
            print(f"Can't find product {search_query} on Wollplatz")
            return
        tree = self.build_lxml_tree(json_data["resultsPanel"]["html"])

        # Here i just assumed that the first product is the one we want
        search_product = self.parse_xpath(
            tree, SearchPaths.search_products, _all=True
        )
        name_url_map = [
            (u.get("title"), u.get("href")) for u in search_product
        ]
        search_product = next(
            url for title, url in name_url_map if title.lower().startswith(search_query.brand_name.lower())
        )
        if not search_product:
            # TODO: error logging
            return None
        return search_product

    async def parse_product(self, product_url: str) -> dict:
        """Parse a product page on the Wollplatz website"""
        product_page_response = await self.perform_request(
            product_url, headers=RequestData.headers
        )

        tree = self.build_lxml_tree(product_page_response.text)

        product_name = self.parse_xpath(tree, ProductPaths.product_name)
        price = self.parse_xpath(tree, ProductPaths.price)
        currency = self.parse_xpath(tree, ProductPaths.currency)

        # TODO type conversion should be done in parse_xpath method
        availability = bool(self.parse_xpath(tree, ProductPaths.availability))
        needle_size = self.parse_xpath(tree, ProductPaths.needle_size)
        composition = self.parse_xpath(tree, ProductPaths.composition)
        brand = self.parse_xpath(tree, ProductPaths.brand)
        product = WoolProduct(
            url=product_url,
            product_name=product_name,
            brand=brand,
            price=Price(value=price, currency=currency),
            availability=availability,
            needle_size=needle_size,
            composition=composition,
        )
        return product
