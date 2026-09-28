from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from app.models.enums import OrderStatus, PartyType, CustomerType

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id", index=True)
    table_id: int = Field(foreign_key="restauranttable.id", index=True)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    total_amount: float = Field(default=0.0)
    party_type: Optional[PartyType] = None
    customer_type: Optional[CustomerType] = None
    session_token: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", index=True)
    menu_item_id: int = Field(foreign_key="menuitem.id")
    quantity: int = Field(default=1)
    unit_price: float
    item_name: str