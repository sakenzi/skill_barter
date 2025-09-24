from pydantic import BaseModel
from typing import Optional
from app.api.products.schemas.response import ProductResponse
from datetime import datetime


class AllRelatedProductResponse(BaseModel):
    id: int
    product_1: Optional[ProductResponse]
    product_2: Optional[ProductResponse]
    created_at: datetime

    class Config:
        from_attributes=True

