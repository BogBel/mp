class ProductPaths:
    product_name = [
        '//span[@class="variants-title-txt"]/text()',
        '//h1[@id="pageheadertitle"]/text()',
    ]
    price = '//div[@id="ContentPlaceHolder1_divinnerbuyholder"]//span[@class="product-price-amount"]/text()'
    currency = '//div[@id="ContentPlaceHolder1_divinnerbuyholder"]//span[@class="product-price-currency"]/text()'
    availability = '//div[@id="ContentPlaceHolder1_divinnerbuyholder"]//span[@class="stock-green"]/text()'
    needle_size = '//tr[td = "Nadelstärke"]/td[2]/text()'
    composition = '//tr[td = "Zusammenstellung"]/td[2]/text()'
    brand = '//tr[td = "Marke"]/td[2]/a/@title'


class SearchPaths:
    search_products = '//a[@class="productlist-imgholder"]'


class RequestData:
    headers = {
        # TODO: User-agent should be randomised
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.5",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.wollplatz.de/",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
    search_params = {
        "type": "suggest",
        "filterInitiated": "false",
        "triggerFilter": "",
        "triggerFilterValue": "",
        "triggerFilterIndex": "",
        "filtersShowAll": "false",
        "enableFiltersShowAll": "false",
        "filterValuesShowAll": "",
        "securedFiltersHash": "false",
        "sortBy": "0",
        "offset": "0",
        "limit": "16",
        "requestIndex": "0",
        "locale": "nl_NL",
        "url": "/",
        # Fields below hardcoded, but can be retrieved from
        # https://static.sooqr.com/custom/119572/1.js?domain=www.wollplatz.de
        "index": "collection:19572",
        "view": "44898be26662b0df",
        "account": "SQ-119572-1",
    }
    search_url = "https://dynamic.sooqr.com/suggest/script/"
    home_url = "https://www.wollplatz.de/"
