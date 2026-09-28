from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.restaurant import AdminUser
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from app.crud import crud_order

router = APIRouter(prefix="/orders", tags=["Order Engine"])

@router.post("/", response_model=OrderRead)
def place_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db)
) -> Any:
    return crud_order.create_order(db=db, order_in=order_in)

@router.get("/{order_id}", response_model=OrderRead)
def get_order_status(
    order_id: int,
    db: Session = Depends(get_db)
) -> Any:
    order = crud_order.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/", response_model=List[OrderRead])
def list_restaurant_orders(
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    return crud_order.get_orders_by_restaurant(db=db, restaurant_id=current_admin.restaurant_id)

@router.put("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    status_in: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
) -> Any:
    order = crud_order.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.restaurant_id != current_admin.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")
    return crud_order.update_order_status(db=db, db_order=order, status_in=status_in)