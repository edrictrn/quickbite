from pydantic import BaseModel
from typing import Optional

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CreateCategoryRequest(BaseModel):
    name: str

class ItemRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    is_available: bool = True

class ItemUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    is_available: Optional[bool] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[str]
    is_available: bool
    category: Optional[CategoryResponse]

    class Config:
        from_attributes = True