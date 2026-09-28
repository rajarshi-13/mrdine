from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.order import OrderStatus

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    special_instructions: Optional[str] = None

class OrderCreate(BaseModel):
    restaurant_id: int
    table_number: str
    customer_name: Optional[str] = None
    items: List[OrderItemCreate]

class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    item_name: str
    price: float
    quantity: int
    special_instructions: Optional[str] = None

    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: int
    restaurant_id: int
    table_number: str
    customer_name: Optional[str] = None
    status: OrderStatus
    total_amount: float
    created_at: datetime
    items: List[OrderItemRead]

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus