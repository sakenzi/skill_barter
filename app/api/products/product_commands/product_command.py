from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from app.api.products.product_crud import product_crud


async def bll_create_product(product_data: dict, db: AsyncSession): 
    subsubcategory = await product_crud.dal_get_subsubcategory(product_data["product_subsubcategory_id"], db)
    if not subsubcategory:
        raise HTTPException(status_code=404, detail="SubSubCategory not found")
    
    exchange_subsubcategory = await product_crud.dal_get_subsubcategory(product_data["exchange_item_subsubcategory_id"], db)
    if not exchange_subsubcategory:
        raise HTTPException(status_code=404, detail="Exchange SubSubCategory not found")
    
    type_product = await product_crud.dal_get_type_product(product_data["type_product_id"], db)
    if not type_product:
        raise HTTPException(status_code=404, detail="TypeProduct not found")
    
    user = await product_crud.dal_get_user(product_data["user_id"], db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return await product_crud.dal_create_product(product_data, db)


async def bll_get_products_by_user(user_id: int, db: AsyncSession):
    products = await product_crud.dal_get_products_by_user(user_id, db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this user")
    return products


async def bll_get_products(db: AsyncSession):
    products = await product_crud.dal_get_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products")
    return products


async def bll_get_product_by_id(product_id: int, db: AsyncSession):
    product = await product_crud.dal_get_product_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product