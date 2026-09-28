from typing import Optional
from pydantic import BaseModel
from app.models.menu import ItemCategory

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: ItemCategory = ItemCategory.MAINS
    is_available: bool = True
    image_url: Optional[str] = None

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[ItemCategory] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None

class MenuItemRead(MenuItemBase):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True