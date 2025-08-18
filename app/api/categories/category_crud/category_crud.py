from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from model.models import ProductCategory, ProductSubCategory, ProductSubSubCategory


async def dal_get_categories(db: AsyncSession):
    res = await db.execute(select(ProductCategory))
    return res.scalars().all()


async def dal_get_subcategories(category_id: int, db: AsyncSession):
    res = await db.execute(
        select(ProductSubCategory).where(ProductSubCategory.product_category_id == category_id))
    return res.scalars().all()


async def dal_get_sub_subcategories(subcategory_id: int, db: AsyncSession):
    res = await db.execute(
        select(ProductSubSubCategory).where(ProductSubSubCategory.product_subcategory_id == subcategory_id)
    )
    return res.scalars().all()