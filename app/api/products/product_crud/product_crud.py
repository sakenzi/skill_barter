from sqlalchemy.ext.asyncio import AsyncSession
from model.models import Product, ProductSubSubCategory, TypeProduct, User, Photo, ProductPhoto
from sqlalchemy import select
from datetime import datetime
from typing import List
from fastapi import UploadFile
import os
import uuid


async def dal_create_product(
    product_data: dict,
    photos: List[UploadFile],
    db: AsyncSession
) -> Product:
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
    await db.flush()  

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    product_photos = []

    for photo_file in photos:
        file_extension = photo_file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(upload_dir, file_name)

        content = await photo_file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        new_photo = Photo(photo=file_path)
        db.add(new_photo)
        await db.flush()  

        product_photos.append(ProductPhoto(
            product_id=new_product.id,
            photo_id=new_photo.id
        ))

    db.add_all(product_photos)
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


async def dal_get_products(db: AsyncSession) -> list[Product]:
    res = await db.execute(
        select(Product)
    )
    return res.scalars().all()


async def dal_get_product_by_id(product_id: int, db: AsyncSession) -> Product | None:
    res = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    return res.scalar_one_or_none()
    