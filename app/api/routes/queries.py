import json

from fastapi import APIRouter

from app.models.query_product import QueryProduct

router = APIRouter()


@router.get("/search_queries")
async def get_products():
    with open("products.json", "r") as file:
        products_data = json.load(file)
    products = [QueryProduct(**product) for product in products_data]
    return products
