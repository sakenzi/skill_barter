from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from model.models import Product, ProductSubSubCategory, TypeProduct, User, Photo, ProductPhoto, RelatedProduct
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from datetime import datetime
from typing import List
from fastapi import UploadFile
import os
import uuid
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        select(Product)
        .where(Product.user_id == user_id)
        .options(
            joinedload(Product.product_photos).joinedload(ProductPhoto.photo),
            joinedload(Product.type_product),
            joinedload(Product.subsubcategory),
            joinedload(Product.exchange_item_subsubcategory),
            joinedload(Product.user).joinedload(User.user_email)
        )
    )
    return res.unique().scalars().all()


async def dal_get_products(db: AsyncSession) -> list[Product]:
    res = await db.execute(
        select(Product)
        .options(
            joinedload(Product.product_photos).joinedload(ProductPhoto.photo),
            joinedload(Product.type_product),
            joinedload(Product.subsubcategory),
            joinedload(Product.exchange_item_subsubcategory),
            joinedload(Product.user).joinedload(User.user_email)
        )
    )
    return res.unique().scalars().all()


async def dal_get_product_by_id(product_id: int, db: AsyncSession) -> Product | None:
    res = await db.execute(
        select(Product)
        .where(Product.id == product_id)
        .options(
            joinedload(Product.product_photos).joinedload(ProductPhoto.photo),
            joinedload(Product.type_product),
            joinedload(Product.subsubcategory),
            joinedload(Product.exchange_item_subsubcategory),
            joinedload(Product.user).joinedload(User.user_email)
        )
    )
    return res.unique().scalar_one_or_none()


def dal_find_all_matching_product(db: Session) -> list[RelatedProduct]:
    try: 
        products = db.execute(
            select(Product)
            .options(
                joinedload(Product.subsubcategory),
                joinedload(Product.exchange_item_subsubcategory),
                joinedload(Product.user)
            )
        ).unique().scalars().all()

        related_products = []

        for product in products:
            matching_products = db.execute(
                select(Product)
                .where(
                    and_(
                        Product.id != product.id,
                        Product.user_id != product.user_id,
                        Product.product_subsubcategory_id == product.exchange_item_subsubcategory_id,
                        Product.exchange_item_subsubcategory_id == product.product_subsubcategory_id
                    )
                )
                .options(
                    joinedload(Product.product_photos).joinedload(ProductPhoto.photo),
                    joinedload(Product.type_product),
                    joinedload(Product.subsubcategory),
                    joinedload(Product.exchange_item_subsubcategory),
                    joinedload(Product.user).joinedload(User.user_email)
                )
            ).unique().scalars().all()

            for match in matching_products:
                try:
                    existing_relation = db.execute(
                        select(RelatedProduct).where(
                            and_(
                                RelatedProduct.product_id_1 == product.id,
                                RelatedProduct.product_id_2 == match.id
                            )
                        )
                    ).scalar_one_or_none()
                    if existing_relation:
                        logger.debug(f"Related product pair {product.id} - {match.id} already exists")
                        continue 

                    related_product = RelatedProduct(
                        product_id_1=product.id,
                        product_id_2=match.id,
                        created_at=datetime.utcnow()
                    )
                    db.add(related_product)
                    db.commit()
                    db.refresh(related_product)
                    related_products.append(related_product)
                    logger.debug(f"Created related product pair: {product.id}-{match.id}")
                except Exception as e:
                    logger.error(f"Failed to create related product pair {product.id}-{match.id}: {str(e)}")
                    db.rollback()

        logger.info(f"Created {len(related_products)} related product pairs")
        return related_products
    except Exception as e:
        logger.error(f"Error in dal_find_all_matching_products: {str(e)}")
        db.rollback()