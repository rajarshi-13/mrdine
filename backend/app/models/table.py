from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from app.models.enums import TableStatus, PartyType, CustomerType

class RestaurantTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id", index=True)
    table_number: int
    status: TableStatus = Field(default=TableStatus.AVAILABLE)
    current_session_token: Optional[str] = None
    session_start_time: Optional[datetime] = None
    party_type: Optional[PartyType] = None
    customer_type: Optional[CustomerType] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))