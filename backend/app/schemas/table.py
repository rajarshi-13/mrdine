from typing import Optional
from pydantic import BaseModel

class RestaurantTableBase(BaseModel):
    table_number: str
    capacity: Optional[int] = 4

class RestaurantTableCreate(RestaurantTableBase):
    pass

class RestaurantTableUpdate(BaseModel):
    table_number: Optional[str] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None

class RestaurantTableRead(RestaurantTableBase):
    id: int
    restaurant_id: int
    qr_code_url: Optional[str] = None
    is_active: bool