from pydantic import BaseModel
from typing import Optional


class CategoryResponse(BaseModel):
    id: int
    category_name: Optional[str] 

    class Config:
        from_attributes=True


class SubCategoryResponse(BaseModel):
    id: int
    subcategory_name: Optional[str]

    class Config:
        from_attributes=True


class SubSubCategoryResponse(BaseModel):
    id: int
    sub_subcategoty_name: Optional[str]

    class Config:
        from_attributes=True