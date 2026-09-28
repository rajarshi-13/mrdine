from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_db
from app.schemas.restaurant import RestaurantCreate, RestaurantRead, AdminCreate
from app.crud import crud_restaurant, crud_admin

router = APIRouter(prefix="/restaurants", tags=["Restaurants & Admins"])

@router.get("/", response_model=List[RestaurantRead])
def list_restaurants(db: Session = Depends(get_db)) -> Any:
    return crud_restaurant.get_restaurants(db)

@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant_in: RestaurantCreate, db: Session = Depends(get_db)) -> Any:
    existing = crud_restaurant.get_restaurant_by_slug(db, slug=restaurant_in.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Restaurant with this slug already exists")
    return crud_restaurant.create_restaurant(db=db, restaurant_in=restaurant_in)

@router.get("/{slug}", response_model=RestaurantRead)
def get_restaurant_by_slug(slug: str, db: Session = Depends(get_db)) -> Any:
    restaurant = crud_restaurant.get_restaurant_by_slug(db, slug=slug)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.post("/admins", status_code=status.HTTP_201_CREATED)
def create_admin(admin_in: AdminCreate, db: Session = Depends(get_db)) -> Any:
    return crud_admin.create_admin(db=db, admin_in=admin_in)