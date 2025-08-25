from fastapi import APIRouter, Depends, Form, UploadFile, File
from app.api.products.product_commands import product_command
from util.service_utils import get_current_user_id
from app.api.products.schemas.create import CreateProduct
from app.api.products.schemas.response import ProductResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from typing import List


router = APIRouter()

@router.post(
    "/",
    summary="Create product"
)
async def create_product(
    product_name: str = Form(...),
    description: str = Form(...),
    exchange_item: str = Form(...),
    product_subsubcategory_id: int = Form(...),
    exchange_item_subsubcategory_id: int = Form(...),
    type_product_id: int = Form(...),
    photos: List[UploadFile] = File([]),
    user_id: int = Depends(get_current_user_id), 
    db: AsyncSession = Depends(get_db)):

    product_data = {
        "product_name": product_name,
        "description": description,
        "exchange_item": exchange_item,
        "product_subsubcategory_id": product_subsubcategory_id,
        "exchange_item_subsubcategory_id": exchange_item_subsubcategory_id,
        "type_product_id": type_product_id,
        "user_id": user_id
    }
    return await product_command.bll_create_product(product_data, photos, db)


@router.get(
    "/my_products",
    summary="Get all products of current user",
    response_model=list[ProductResponse]
)
async def get_products_by_user(user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    return await product_command.bll_get_products_by_user(user_id, db)


@router.get(
    "/",
    summary="Get all products",
    response_model=list[ProductResponse]
)
async def get_products(db: AsyncSession = Depends(get_db)):
    return await product_command.bll_get_products(db)


@router.get(
    "/{product_id}",
    summary="Get product by id",
    response_model=ProductResponse
)
async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    return await product_command.bll_get_product_by_id(product_id, db)