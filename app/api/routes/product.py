# product_router.py
import json

from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.crawlers.wollplatz.crawler import Wollplatz
from app.db.redis import get_products_by_id
from app.models.product_data import ProductData
from app.models.product_types.wool_product import WoolProduct
from app.models.query_product import QueryProduct

router = APIRouter()


@router.get("/all-products", response_model=list[ProductData])
async def get_all_products():
    with open("products.json", "r") as file:
        query_products = json.load(file)
    product_data_list = []
    for query_product in query_products:
        product_details = await get_products_by_id(query_product["id"])
        product_data = ProductData(
            query_data=query_product, products=product_details
        )
        product_data_list.append(product_data)
    return product_data_list


@router.get("/product/{product_id}", response_model=ProductData)
async def get_product(product_id: int):
    with open("products.json") as file:
        query_products = json.load(file)
    query_product = next(
        (item for item in query_products if item["id"] == product_id), None
    )
    if not query_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Fetch product details from Redis
    product_details = await get_products_by_id(product_id)
    product_details = [
        WoolProduct(**product_detail) for product_detail in product_details
    ]

    product_data = ProductData(
        query_data=query_product, products=product_details
    )
    return product_data


@router.post("/product/{product_id}/refresh")
async def refresh_product_data(
    product_id: int, background_tasks: BackgroundTasks
):
    # Fetch product query information
    with open("products.json") as file:
        query_products = json.load(file)
    query_product = next(
        (item for item in query_products if item["id"] == product_id), None
    )

    if not query_product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Here we should check the website name and call the appropriate crawler
    # But it will require better storage of product data etc
    crawler = Wollplatz()

    # Schedule the refresh task
    background_tasks.add_task(
        crawler.search_and_parse, QueryProduct(**query_product)
    )
    return {"message": "Refresh scheduled"}


@router.post("/products/refresh-all")
async def refresh_all_products(background_tasks: BackgroundTasks):
    # Fetch all product query information
    with open("products.json") as file:
        query_products = json.load(file)

    if not query_products:
        raise HTTPException(status_code=404, detail="No products found")

    crawler = Wollplatz()

    # Schedule refresh tasks for each product
    for query_product in query_products:
        background_tasks.add_task(
            crawler.search_and_parse, QueryProduct(**query_product)
        )

    return {"message": "Refresh scheduled for all products"}
