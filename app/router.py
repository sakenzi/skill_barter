from fastapi import APIRouter
from app.api.auth.auth_api import router as auth_router
from app.api.categories.category_api import router as category_router


route = APIRouter()

route.include_router(auth_router, prefix="/auth", tags=["Authentication"])
route.include_router(category_router, prefix="/category", tags=["Category"])