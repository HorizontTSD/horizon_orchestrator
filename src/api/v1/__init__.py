# src/api/v1/__init__.py
from fastapi import APIRouter

from .get_forecast import router as func_get_forecast_data


router = APIRouter()

router.include_router(func_get_forecast_data, tags=["Get Forecast Data"])

