from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.order import Order, OrderItem, OrderStatus
from app.models.menu import MenuItem
from app.schemas.order import OrderCreate, OrderStatusUpdate

def create_order(db: Session, order_in: OrderCreate) -> Order:
    db_order = Order(
        restaurant_id=order_in.restaurant_id,
        table_number=order_in.table_number,
        customer_name=order_in.customer_name,
        status=OrderStatus.PENDING,
        total_amount=0.0
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    total_price = 0.0
    for item in order_in.items:
        menu_item = db.get(MenuItem, item.menu_item_id)
        if not menu_item or menu_item.restaurant_id != order_in.restaurant_id:
            raise HTTPException(status_code=400, detail=f"Menu item {item.menu_item_id} not valid for this restaurant")
        if not menu_item.is_available:
            raise HTTPException(status_code=400, detail=f"Menu item '{menu_item.name}' is currently unavailable")
        
        item_total = menu_item.price * item.quantity
        total_price += item_total
        
        order_item = OrderItem(
            order_id=db_order.id,
            menu_item_id=menu_item.id,
            item_name=menu_item.name,
            price=menu_item.price,
            quantity=item.quantity,
            special_instructions=item.special_instructions
        )
        db.add(order_item)
    
    db_order.total_amount = total_price
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.get(Order, order_id)

def get_orders_by_restaurant(db: Session, restaurant_id: int) -> List[Order]:
    return db.exec(select(Order).where(Order.restaurant_id == restaurant_id).order_by(Order.created_at.desc())).all()

def update_order_status(db: Session, db_order: Order, status_in: OrderStatusUpdate) -> Order:
    db_order.status = status_in.status
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order