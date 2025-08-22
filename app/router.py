from fastapi import APIRouter
from app.api.auth.auth_api import router as auth_router
from app.api.categories.category_api import router as category_router
from app.api.products.product_api import router as product_router


route = APIRouter()

route.include_router(auth_router, prefix="/auth", tags=["Authentication"])
route.include_router(category_router, prefix="/category", tags=["Category"])
route.include_router(product_router, prefix="/product", tags=["Product"])