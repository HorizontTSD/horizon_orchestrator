# src/api/v1/proxy_schedule_forecast/router.py
from fastapi import APIRouter
from src.api.v1.proxy_schedule_forecast import endpoints, dbconnection_endpoints, schedule_forecast_endpoints, metrics_endpoints #, get_tables_info_endpoint

router = APIRouter(prefix="/proxy_schedule_forecast", tags=["Proxy Schedule Forecast"])

router.include_router(dbconnection_endpoints.router)
router.include_router(schedule_forecast_endpoints.router)
router.include_router(metrics_endpoints.router)
router.include_router(endpoints.router)