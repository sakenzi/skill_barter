from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from app.api.categories.category_commands import category_command
from app.api.categories.schemas.response import CategoryResponse, SubCategoryResponse, SubSubCategoryResponse


router = APIRouter()

@router.get(
    "/categories",
    response_model=list[CategoryResponse],
    summary="Get all categories"
)
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await category_command.bll_get_categories(db=db)


@router.get(
    "/subcategories",
    response_model=list[SubCategoryResponse],
    summary="Get all subcategories"
)
async def get_subcategories(category_id: int, db: AsyncSession = Depends(get_db)):
    return await category_command.bll_get_subcategories(category_id=category_id, db=db)


@router.get(
    "/sub_subcategories",
    response_model=list[SubSubCategoryResponse],
    summary="Get all sub_subcategories"
)
async def get_sub_subcategories(subcategory_id: int, db: AsyncSession = Depends(get_db)):
    return await category_command.bll_get_sub_subcategories(subcategory_id=subcategory_id, db=db)