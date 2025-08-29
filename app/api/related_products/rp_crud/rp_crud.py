from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from model.models import RelatedProduct, Product, ProductPhoto, User, UserEmail
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def dal_get_all_related_products(db: AsyncSession) -> list[RelatedProduct]:
    res = await db.execute(
        select(RelatedProduct)
        .options(
            joinedload(RelatedProduct.product_1)
            .options(
                joinedload(Product.product_photos).joinedload(ProductPhoto.photo),
                joinedload(Product.type_product),
                joinedload(Product.subsubcategory),
                joinedload(Product.exchange_item_subsubcategory),
                joinedload(Product.user).joinedload(User.user_email)
            ),
            joinedload(RelatedProduct.product_2)
            .options(
                joinedload(Product.product_photos).joinedload(ProductPhoto.photo),
                joinedload(Product.type_product),
                joinedload(Product.subsubcategory),
                joinedload(Product.exchange_item_subsubcategory),
                joinedload(Product.user).joinedload(User.user_email)
            )
        )
    )
    related_products = res.unique().scalars().all()
    return related_products