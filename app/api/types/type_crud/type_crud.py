from sqlalchemy.ext.asyncio import AsyncSession
from model.models import TypeProduct
from sqlalchemy import select


async def dal_create_type_product(type_name: str, db: AsyncSession) -> TypeProduct:
    new_type = TypeProduct(type_name=type_name)
    db.add(new_type)
    await db.commit()
    await db.refresh(new_type)
    return new_type


async def dal_get_all_type_product(db: AsyncSession):
    res = await db.execute(select(TypeProduct))
    return res.scalars().all()