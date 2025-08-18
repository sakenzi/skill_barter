from pydantic import BaseModel


class CategoryCreate(BaseModel):
    category_name: str


class SubCategoryCreate(BaseModel):
    subcategory_name: str
    category_id: int


class SubSubCategoryCreate(BaseModel):
    sub_subcategory_name: str
    subcategory_id: int