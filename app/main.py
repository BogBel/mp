from fastapi import FastAPI
from app.api.routes.queries import router as queries_router
from app.api.routes.product import router as product_router

app = FastAPI()

app.include_router(queries_router, prefix="/api")
app.include_router(product_router, prefix="/api")
