from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserEmailResponse(BaseModel):
    email: str

    class Config:
        from_attributes=True


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    surname: Optional[str] = None
    phone_number: str

    user_email: Optional[UserEmailResponse] 

    class Config:
        from_attributes=True


class PhotoResponse(BaseModel):
    id: int
    photo: str

    class Config:
        from_attributes=True


class TypeProductResponse(BaseModel):
    id: int
    type_name: str

    class Config:
        from_attributes=True

    
class ProductSubSubCategoryResponse(BaseModel):
    id: int
    sub_subcategory_name: str
    subcategory_id: int

    class Config: 
        from_attributes=True


class ProductResponse(BaseModel):
    id: int
    product_name: Optional[str]
    description: str
    exchange_item: Optional[str]
    created_at: datetime
    updated_at: datetime

    photos: List[PhotoResponse] = []
    type_product: Optional[TypeProductResponse]
    subsubcategory: Optional[ProductSubSubCategoryResponse]
    exchange_item_subsubcategory: Optional[ProductSubSubCategoryResponse]
    user: Optional[UserResponse]

    class Config:
        from_attributes=True