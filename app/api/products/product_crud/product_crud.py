from sqlalchemy.ext.asyncio import AsyncSession
from model.models import Product


async def dal_create_product(product_data: dict, db: AsyncSession) -> Product:
    new_product = Product(**product_data)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product