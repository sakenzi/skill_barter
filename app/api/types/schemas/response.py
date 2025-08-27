from pydantic import BaseModel
from typing import Optional


class TypeResponse(BaseModel):
    id: int
    type_name: str

    class Config:
        from_attributes=True