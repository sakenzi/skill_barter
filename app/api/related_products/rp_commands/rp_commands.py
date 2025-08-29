from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.api.related_products.rp_crud import rp_crud


async def bll_get_all_related_products(db: AsyncSession):
    related_products = await rp_crud.dal_get_all_related_products(db)
    if not related_products:
        raise HTTPException(status_code=404, detail="No related product pairs found")
    return related_products