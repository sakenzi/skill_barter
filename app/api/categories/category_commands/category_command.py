from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.api.categories.category_crud import category_crud


async def bll_get_categories(db: AsyncSession):
    categories = await category_crud.dal_get_categories(db)
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return categories


async def bll_get_subcategories(category_id: int, db: AsyncSession):
    subcategories = await category_crud.dal_get_subcategories(category_id, db)
    if not subcategories:
        raise HTTPException(status_code=404, detail="No subcategories found for this category")
    return subcategories


async def bll_get_sub_subcategories(subcategory_id: int, db: AsyncSession):
    sub_subcategories = await category_crud.dal_get_sub_subcategories(subcategory_id, db)
    if not sub_subcategories:
        raise HTTPException(status_code=404, detail="No sub-subcategories found for this subcategory")
    return sub_subcategories


async def bll_create_category(category_name: str, db: AsyncSession):
    return await category_crud.dal_create_category(category_name, db)


async def bll_create_subcategory(subcategory_name: str, category_id: int, db: AsyncSession):
    categories = await category_crud.dal_get_categories(db)
    if not any(c.id == category_id for c in categories):
        raise HTTPException(404, detail="Category not found")
    return await category_crud.dal_create_subcategory(subcategory_name, category_id, db)


async def bll_create_sub_subcategory(sub_subcategory_name: str, subcategory_id: int, db: AsyncSession):
    subcategories = await category_crud.dal_get_subcategories(subcategory_id, db)
    if not subcategories:
        raise HTTPException(404, detail="Subcategory not found")
    return await category_crud.dal_create_sub_subcategory(sub_subcategory_name, subcategory_id, db)
