from typing import Optional
from pydantic import BaseModel

class RestaurantBase(BaseModel):
    name: str
    slug: str
    address: Optional[str] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantRead(RestaurantBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class AdminCreate(BaseModel):
    restaurant_id: int
    username: str
    password: str

class AdminRead(BaseModel):
    id: int
    restaurant_id: int
    username: str
    is_active: bool

    class Config:
        from_attributes = True