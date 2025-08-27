from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter
from app.api.types.type_command import type_command
from app.api.types.schemas.response import TypeResponse
from db.database import get_db


router = APIRouter()

@router.post(
    "/",
    summary="Create type product",
    response_model=TypeResponse
)
async def create_product(type_name: str, db: AsyncSession = Depends(get_db)):
    return await type_command.bll_create_type_product(type_name=type_name, db=db)


@router.get(
    "/",
    summary="Get all type products",
    response_model=list[TypeResponse]
)   
async def get_all_type_product(db: AsyncSession = Depends(get_db)):
    return await type_command.bll_get_all_type_product(db=db)