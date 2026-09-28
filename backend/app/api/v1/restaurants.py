from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_db
from app.core.security import get_password_hash, create_access_token
from app.models.restaurant import Restaurant, AdminUser
from app.schemas.restaurant import RestaurantCreate, RestaurantRead, AdminCreate, AdminRead

router = APIRouter(prefix="/restaurants", tags=["Restaurants & Admins"])

@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant_in: RestaurantCreate, db: Session = Depends(get_db)):
    existing = db.exec(select(Restaurant).where(Restaurant.slug == restaurant_in.slug)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Restaurant slug already exists")
    restaurant = Restaurant(name=restaurant_in.name, slug=restaurant_in.slug)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.get("/", response_model=List[RestaurantRead])
def list_restaurants(db: Session = Depends(get_db)):
    return db.exec(select(Restaurant)).all()

@router.get("/{slug}", response_model=RestaurantRead)
def get_restaurant_by_slug(slug: str, db: Session = Depends(get_db)):
    restaurant = db.exec(select(Restaurant).where(Restaurant.slug == slug)).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.post("/admins", response_model=AdminRead, status_code=status.HTTP_201_CREATED)
def create_admin(admin_in: AdminCreate, db: Session = Depends(get_db)):
    restaurant = db.get(Restaurant, admin_in.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    existing_user = db.exec(select(AdminUser).where(AdminUser.username == admin_in.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    admin = AdminUser(
        restaurant_id=admin_in.restaurant_id,
        username=admin_in.username,
        hashed_password=get_password_hash(admin_in.password)
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin