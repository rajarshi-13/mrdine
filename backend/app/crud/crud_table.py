from typing import List, Optional
from sqlmodel import Session, select
from app.models.table import RestaurantTable

def create_table(db: Session, table_in: RestaurantTable, restaurant_id: int) -> RestaurantTable:
    db_table = RestaurantTable(
        restaurant_id=restaurant_id,
        table_number=table_in.table_number,
        capacity=table_in.capacity,
        qr_code_url=table_in.qr_code_url,
        is_active=table_in.is_active
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_tables_by_restaurant(db: Session, restaurant_id: int) -> List[RestaurantTable]:
    return db.exec(select(RestaurantTable).where(RestaurantTable.restaurant_id == restaurant_id)).all()

def get_table(db: Session, table_id: int) -> Optional[RestaurantTable]:
    return db.get(RestaurantTable, table_id)

def update_table(db: Session, db_table: RestaurantTable, table_in: RestaurantTable) -> RestaurantTable:
    table_data = table_in.model_dump(exclude_unset=True)
    db_table.sqlmodel_update(table_data)
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def delete_table(db: Session, db_table: RestaurantTable) -> RestaurantTable:
    db.delete(db_table)
    db.commit()
    return db_table