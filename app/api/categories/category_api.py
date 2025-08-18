from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from app.api.categories.category_commands import category_command
from app.api.categories.schemas.response import CategoryResponse, SubCategoryResponse, SubSubCategoryResponse
from app.api.categories.schemas.create import CategoryCreate, SubCategoryCreate, SubSubCategoryCreate


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


@router.post(
    "/categories",
    response_model=CategoryCreate,
    summary="Create category"
)
async def create_category(category_name: str, db: AsyncSession = Depends(get_db)):
    return await category_command.bll_create_category(category_name=category_name, db=db)


@router.post(
    "/subcategories",
    response_model=SubCategoryCreate,
    summary="Create subcategory"
)
async def create_subcategory(subcategory_name: str, category_id: int, db: AsyncSession = Depends(get_db)):
    return await category_command.bll_create_subcategory(subcategory_name=subcategory_name, category_id=category_id, db=db)


@router.post(
    "/sub_subcategories",
    response_model=SubSubCategoryCreate,
    summary="Create sub_subcategory"
)
async def create_sub_subcategory(sub_subcategory_name: str, subcategory_id: int, db: AsyncSession = Depends(get_db)):
    return await category_command.bll_create_sub_subcategory(sub_subcategory_name=sub_subcategory_name, subcategory_id=subcategory_id, db=db)