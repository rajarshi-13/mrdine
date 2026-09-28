from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.restaurant import AdminUser
from app.models.menu import MenuItem
from app.schemas.menu import MenuItemCreate, MenuItemRead, MenuItemUpdate
from app.crud import crud_menu

router = APIRouter(prefix="/menu", tags=["Menu Management"])

@router.get("/", response_model=List[MenuItemRead])
def read_items(
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    return crud_menu.get_menu_items_by_restaurant(db, restaurant_id=current_admin.restaurant_id)

@router.post("/", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: MenuItemCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    return crud_menu.create_menu_item(db=db, item_in=item_in, restaurant_id=current_admin.restaurant_id)

@router.put("/{item_id}", response_model=MenuItemRead)
def update_item(
    item_id: int,
    item_in: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    db_item = crud_menu.get_menu_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    if db_item.restaurant_id != current_admin.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this item")
    return crud_menu.update_menu_item(db=db, db_item=db_item, item_in=item_in)

@router.delete("/{item_id}", response_model=MenuItemRead)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    db_item = crud_menu.get_menu_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    if db_item.restaurant_id != current_admin.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")
    return crud_menu.delete_menu_item(db=db, db_item=db_item)