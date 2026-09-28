from typing import List, Optional
from sqlmodel import Session, select
from app.models.menu import MenuItem
from app.schemas.menu import MenuItemCreate, MenuItemUpdate

def create_menu_item(db: Session, item_in: MenuItemCreate, restaurant_id: int) -> MenuItem:
    db_item = MenuItem.model_validate(item_in, update={"restaurant_id": restaurant_id})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_menu_items_by_restaurant(db: Session, restaurant_id: int) -> List[MenuItem]:
    return db.exec(select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)).all()

def get_menu_item(db: Session, item_id: int) -> Optional[MenuItem]:
    return db.get(MenuItem, item_id)

def update_menu_item(db: Session, db_item: MenuItem, item_in: MenuItemUpdate) -> MenuItem:
    item_data = item_in.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_menu_item(db: Session, db_item: MenuItem) -> MenuItem:
    db.delete(db_item)
    db.commit()
    return db_item