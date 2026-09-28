from fastapi import FastAPI
from app.core.database import init_db
from app.api.v1.api import api_router
# Import SQLModel models so they are registered before table creation
from app.models.restaurant import Restaurant, AdminUser
from app.models.table import RestaurantTable
from app.models.menu import MenuItem
from app.models.order import Order, OrderItem

app = FastAPI(title="Mr. Dine API", version="0.1.0")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Mr. Dine API"}

@app.get("/api/v1/ping")
def ping():
    return {"ping": "pong"}