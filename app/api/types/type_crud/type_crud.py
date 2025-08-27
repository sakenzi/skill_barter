from sqlalchemy.ext.asyncio import AsyncSession
from model.models import TypeProduct


async def dal_create_type_product(type_name: str, db: AsyncSession) -> TypeProduct:
    new_type = TypeProduct(type_name=type_name)
    db.add(new_type)
    await db.commit()
    await db.refresh(new_type)
    return new_type