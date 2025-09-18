# src/api/api_router.py
from fastapi import APIRouter
from src.api.v1.greeting import router as greeting_router
from src.api.v1.proxy_schedule_forecast.router import router as proxy_schedule_forecast_router

api_router = APIRouter()

api_router.include_router(greeting_router, prefix="/greetings", tags=["Greetings"])
api_router.include_router(proxy_schedule_forecast_router, prefix="")
