from typing import List, Optional
from sqlmodel import Session, select
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate

def create_restaurant(db: Session, restaurant_in: RestaurantCreate) -> Restaurant:
    db_obj = Restaurant.model_validate(restaurant_in)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_restaurants(db: Session) -> List[Restaurant]:
    return db.exec(select(Restaurant)).all()

def get_restaurant_by_slug(db: Session, slug: str) -> Optional[Restaurant]:
    return db.exec(select(Restaurant).where(Restaurant.slug == slug)).first()