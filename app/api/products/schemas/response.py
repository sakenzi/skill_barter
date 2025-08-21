from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductResponse(BaseModel):
    id: int
    product_name: Optional[str]
    description: str
    exchange_item: Optional[str]
    product_subsubcategory_id: int
    exchange_item_subsubcategory_id: int
    type_product_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True