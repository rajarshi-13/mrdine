from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RestaurantCreate(BaseModel):
    name: str
    slug: str

class RestaurantRead(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime

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