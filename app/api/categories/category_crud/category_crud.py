from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from model.models import ProductCategory, ProductSubCategory, ProductSubSubCategory


async def dal_get_categories(db: AsyncSession):
    res = await db.execute(select(ProductCategory))
    return res.scalars().all()


async def dal_get_subcategories(category_id: int, db: AsyncSession):
    res = await db.execute(
        select(ProductSubCategory).where(ProductSubCategory.category_id == category_id))
    return res.scalars().all()


async def dal_get_sub_subcategories(subcategory_id: int, db: AsyncSession):
    res = await db.execute(
        select(ProductSubSubCategory).where(ProductSubSubCategory.subcategory_id == subcategory_id)
    )
    return res.scalars().all()


async def dal_create_category(category_name: str, db: AsyncSession) -> ProductCategory:
    new_category = ProductCategory(category_name=category_name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


async def dal_create_subcategory(subcategory_name: str, category_id: int, db: AsyncSession) -> ProductSubCategory:
    new_subcategory = ProductSubCategory(subcategory_name=subcategory_name, category_id=category_id)
    db.add(new_subcategory)
    await db.commit()
    await db.refresh(new_subcategory)
    return new_subcategory


async def dal_create_sub_subcategory(sub_subcategory_name: str, subcategory_id: int, db: AsyncSession) -> ProductSubSubCategory:
    new_sub_subcategory = ProductSubSubCategory(sub_subcategory_name=sub_subcategory_name, subcategory_id=subcategory_id)
    db.add(new_sub_subcategory)
    await db.commit()
    await db.refresh(new_sub_subcategory)
    return new_sub_subcategory