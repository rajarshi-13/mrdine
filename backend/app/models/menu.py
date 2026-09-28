from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field

class ItemCategory(str, Enum):
    APPETIZERS = "APPETIZERS"
    MAINS = "MAINS"
    DESSERTS = "DESSERTS"
    BEVERAGES = "BEVERAGES"
    SIDES = "SIDES"

class MenuItem(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    name: str
    description: Optional[str] = None
    price: float
    category: ItemCategory = Field(default=ItemCategory.MAINS)
    is_available: bool = Field(default=True)
    image_url: Optional[str] = None