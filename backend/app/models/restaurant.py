from typing import Optional
from sqlmodel import SQLModel, Field

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    slug: str = Field(unique=True, index=True)
    address: Optional[str] = None
    is_active: bool = Field(default=True)

class AdminUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)