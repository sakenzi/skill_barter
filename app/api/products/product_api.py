from fastapi import APIRouter, Depends, Request
from app.api.products.product_commands import product_command
from util.service_utils import validate_token, get_access_token
from app.api.products.schemas.create import CreateProduct
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db


router = APIRouter()

@router.post(
    "/create",
    summary="Create product"
)
async def create_product(
    product: CreateProduct,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    access_token = get_access_token(request)
    user = await validate_token(access_token, db)
    
    product_data = product.dict()
    product_data["user_id"] = user.id  
    
    return await product_command.bll_create_product(product_data, db)