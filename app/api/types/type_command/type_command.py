from sqlalchemy.ext.asyncio import AsyncSession
from app.api.types.type_crud import type_crud
from fastapi import HTTPException


async def bll_create_type_product(type_name: str, db: AsyncSession):
    return await type_crud.dal_create_type_product(type_name, db)