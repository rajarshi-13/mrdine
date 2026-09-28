from typing import Optional
from sqlmodel import SQLModel, Field

class RestaurantTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    table_number: str
    capacity: Optional[int] = Field(default=4)
    qr_code_url: Optional[str] = None
    is_active: bool = Field(default=True)