import json
import redis.asyncio as redis
from app.models.product import Product

from app.settings import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


async def get_products_by_id(product_id: int) -> list[str]:
    redis_pattern = f"query:{product_id}:*"
    product_keys = [key async for key in redis_client.scan_iter(match=redis_pattern)]
    if product_keys:
        product_details = list(map(json.loads, await redis_client.mget(product_keys)))
    else:
        product_details = []
    return product_details
