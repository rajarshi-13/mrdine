from fastapi import APIRouter
from app.api.v1.restaurants import router as restaurants_router

api_router = APIRouter()
api_router.include_router(restaurants_router)