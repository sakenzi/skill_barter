import logging
from celery import shared_task
from config.celery_config import app
from sqlalchemy.orm import joinedload
from db.database import SessioLocal
from app.api.products.product_crud import product_crud


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@shared_task
def find_all_matching_products_task():
    try:
        with SessioLocal() as db:
            related_products = product_crud.dal_find_all_matching_product(db)
        logger.info(f"Task completed: Created {len(related_products)} related product pairs")
        return [rp.id for rp in related_products]
    except Exception as e:
        logger.error(f"Error in find_all_matching_products_task: {str(e)}")
        raise