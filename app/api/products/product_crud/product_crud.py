from sqlalchemy.ext.asyncio import AsyncSession
from model.models import Product, ProductSubSubCategory, TypeProduct, User
from sqlalchemy import select
from datetime import datetime


async def dal_create_product(product_data: dict, db: AsyncSession) -> Product:
    new_product = Product(
        product_name=product_data["product_name"],
        description=product_data["description"],
        exchange_item=product_data["exchange_item"],
        product_subsubcategory_id=product_data["product_subsubcategory_id"],
        exchange_item_subsubcategory_id=product_data["exchange_item_subsubcategory_id"],
        type_product_id=product_data["type_product_id"],
        user_id=product_data["user_id"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


async def dal_get_subsubcategory(subsubcategory_id: int, db: AsyncSession) -> ProductSubSubCategory | None:
    res = await db.execute(
        select(ProductSubSubCategory).where(ProductSubSubCategory.id == subsubcategory_id)
    )
    return res.scalar_one_or_none()


async def dal_get_type_product(type_product_id: int, db: AsyncSession) -> TypeProduct | None:
    res = await db.execute(
        select(TypeProduct).where(TypeProduct.id == type_product_id)
    )
    return res.scalar_one_or_none()


async def dal_get_user(user_id: int, db: AsyncSession) -> User | None:
    res = await db.execute(
        select(User).where(User.id == user_id)
    )
    return res.scalar_one_or_none()


async def dal_get_products_by_user(user_id: int, db: AsyncSession) -> list[Product]:
    res = await db.execute(
        select(Product).where(Product.user_id == user_id))
    return res.scalars().all()