from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_db
from app.models.restaurant import AdminUser
from app.schemas.table import RestaurantTableCreate, RestaurantTableRead, RestaurantTableUpdate
from app.crud import crud_table
from app.api.deps import get_current_admin

router = APIRouter(prefix="/tables", tags=["Table & QR Management"])

@router.post("/", response_model=RestaurantTableRead, status_code=status.HTTP_201_CREATED)
def create_new_table(
    table_in: RestaurantTableCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
) -> Any:
    return crud_table.create_table(db=db, table_in=table_in, restaurant_id=current_admin.restaurant_id)

@router.get("/", response_model=List[RestaurantTableRead])
def read_tables(
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
) -> Any:
    return crud_table.get_tables_by_restaurant(db=db, restaurant_id=current_admin.restaurant_id)

@router.put("/{table_id}", response_model=RestaurantTableRead)
def update_existing_table(
    table_id: int,
    table_in: RestaurantTableUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
) -> Any:
    table = crud_table.get_table(db=db, table_id=table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    if table.restaurant_id != current_admin.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this table")
    return crud_table.update_table(db=db, db_table=table, table_in=table_in)

@router.delete("/{table_id}", response_model=RestaurantTableRead)
def delete_existing_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
) -> Any:
    table = crud_table.get_table(db=db, table_id=table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    if table.restaurant_id != current_admin.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this table")
    return crud_table.delete_table(db=db, db_table=table)