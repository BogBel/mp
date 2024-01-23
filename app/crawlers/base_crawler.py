import asyncio
import json
from typing import Any, Optional, Union

import aiohttp
from lxml import etree, html
from selenium import webdriver

from app.db.redis import redis_client
from app.enums.request import Method
from app.exceptions.network import RequestFailed
from app.models.product import Product
from app.models.query_product import QueryProduct
from app.models.response import Response
from app.settings import settings


class BaseCrawler:
    name = None

    async def search(self, search_query):
        raise NotImplementedError

    async def parse_product(self, product_url):
        raise NotImplementedError

    async def perform_request(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[dict[str, str]] = None,
        method: str = "GET",
    ) -> Union[str, None]:
        max_retries = 2
        for attempt in range(max_retries):
            async with aiohttp.ClientSession(cookies=cookies) as session:
                try:
                    async with session.request(
                        method, url, params=params, headers=headers
                    ) as response:
                        # TODO add proper error handling, we don't need to retry on 404 for example
                        response.raise_for_status()
                        text = await response.text()
                        response_data = Response(
                            status_code=response.status,
                            headers=dict(response.headers),
                            cookies={
                                key: value.value
                                for key, value in response.cookies.items()
                            },
                            text=text,
                        )
                        return response_data
                except aiohttp.ClientError as e:
                    print(
                        f"Request failed {url}, attempt {attempt + 1}/{max_retries}. Error: {e}"
                    )
        mock_response = await self.read_response_from_file_by_url(url)
        if mock_response:
            return mock_response
        raise RequestFailed(
            f"Request {url} failed after {max_retries} attempts"
        )

    async def read_response_from_file_by_url(self, url: str) -> str:
        """Read response from file by url"""
        mapping = {
            "https://www.wollplatz.de/artikel/35246/drops-safran-60-moss-green.html": "app/data/drops-safran-60-moss-green.html",
            "https://www.wollplatz.de/wolle/dmc/dmc-natura-xl": "app/data/dmc_natura_xl.html",
            "https://www.wollplatz.de/artikel/35226/drops-baby-merino-mix-48-blush.html": "app/data/drops-baby-merino-mix-48-blush.html",
            "https://www.wollplatz.de/artikel/29382/stylecraft-special-dk-1856-dandelion.html": "app/data/stylecraft-special-dk-1856-dandelion.html",
        }
        file_name = mapping.get(url)
        if not file_name:
            return None
        with open(file_name, "r") as file:
            return Response(
                status_code=200, headers={}, cookies={}, text=file.read()
            )

    async def search_and_parse(
        self, search_query: QueryProduct
    ) -> Union[Product, None]:
        search_results = await self.search(search_query)
        if not search_results:
            return
        product = await self.parse_product(search_results)
        redis_key = f"query:{search_query.id}:{self.name.value}"
        await redis_client.set(
            redis_key,
            product.model_dump_json(),
        )
        await redis_client.expire(
            redis_key,
            settings.product_info_lifetime,
        )
        return product

    def parse_xpath(
        self,
        tree: etree._ElementTree,
        path: Union[str, list[str]],
        _all: bool = False,
        default: Optional[Any] = None,
    ):
        # TODO More advanced error handling and params
        paths = [path] if isinstance(path, str) else path
        for p in paths:
            res = tree.xpath(p)
            if _all:
                return res
            if res:
                return res[0]
        return default

    def build_lxml_tree(self, html_string: str):
        # TODO add error handling
        return html.fromstring(html_string)

    def build_json(self, raw_json: str):
        # TODO add error handling
        return json.loads(raw_json)
