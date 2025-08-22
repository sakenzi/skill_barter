from fastapi import APIRouter, Depends, Request
from app.api.products.product_commands import product_command
from util.service_utils import validate_token, get_access_token, get_current_user_id
from app.api.products.schemas.create import CreateProduct
from app.api.products.schemas.response import ProductResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db


router = APIRouter()

@router.post(
    "/create",
    summary="Create product"
)
async def create_product(product: CreateProduct, user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    product_data = product.dict()
    product_data["user_id"] = user_id  
    return await product_command.bll_create_product(product_data, db)


@router.get(
    "/my_products",
    summary="Get all products of current user",
    response_model=list[ProductResponse]
)
async def get_products_by_user(user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    return await product_command.bll_get_products_by_user(user_id, db)


@router.get(
    "/products",
    summary="Get all products",
    response_model=list[ProductResponse]
)
async def get_products(db: AsyncSession = Depends(get_db)):
    return await product_command.bll_get_products(db)