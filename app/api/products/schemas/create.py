from pydantic import BaseModel, Field
from typing import Optional


class CreateProduct(BaseModel):
    product_name: Optional[str] = Field(max_length=150)
    description: str = Field(..., min_length=20)
    exchange_item: Optional[str] = Field(max_length=150)
    product_subsubcategory_id: int
    exchange_item_subsubcategory_id: int
    type_product_id: int
    user_id: int
