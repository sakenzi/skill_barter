from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter
from app.api.related_products.rp_commands import rp_commands
from app.api.related_products.schemas.response import AllRelatedProductResponse
from db.database import get_db


router = APIRouter()

@router.get(
    "/",
    summary="получить все сопутствующие товары",
    response_model=list[AllRelatedProductResponse]
)
async def get_all_related_products(db: AsyncSession = Depends(get_db)):
    return await rp_commands.bll_get_all_related_products(db)