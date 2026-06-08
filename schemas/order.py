from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemRequest(BaseModel):
    item_id: int
    quantity: int

class CreateOrderRequest(BaseModel):
    items: List[OrderItemRequest]
    note: Optional[str] = None

class OrderItemResponse(BaseModel):
    item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    status: str
    total: float
    note: Optional[str]
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class UpdateOrderStatusRequest(BaseModel):
    status: str
