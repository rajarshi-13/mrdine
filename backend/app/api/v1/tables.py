from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.restaurant import AdminUser
from app.models.table import RestaurantTable
from app.crud import crud_table
from app.core.qr_code import generate_qr_code_image

router = APIRouter(prefix="/tables", tags=["Table & QR Management"])

@router.get("/", response_model=List[RestaurantTable])
def read_tables(
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    return crud_table.get_tables_by_restaurant(db, restaurant_id=current_admin.restaurant_id)

@router.post("/", response_model=RestaurantTable)
def create_table(
    table_in: RestaurantTable,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    return crud_table.create_table(db=db, table_in=table_in, restaurant_id=current_admin.restaurant_id)

@router.put("/{table_id}", response_model=RestaurantTable)
def update_table(
    table_id: int,
    table_in: RestaurantTable,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    db_table = crud_table.get_table(db, table_id=table_id)
    if not db_table:
        raise HTTPException(status_code=404, detail="Table not found")
    if db_table.restaurant_id != current_admin.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this table")
    return crud_table.update_table(db=db, db_table=db_table, table_in=table_in)

@router.delete("/{table_id}", response_model=RestaurantTable)
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    db_table = crud_table.get_table(db, table_id=table_id)
    if not db_table:
        raise HTTPException(status_code=404, detail="Table not found")
    if db_table.restaurant_id != current_admin.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this table")
    return crud_table.delete_table(db=db, db_table=db_table)

@router.get("/{table_id}/qr")
def get_table_qr(
    table_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    table = crud_table.get_table(db, table_id=table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    if table.restaurant_id != current_admin.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    qr_bytes = generate_qr_code_image(table.qr_code_url)
    return Response(content=qr_bytes, media_type="image/png")