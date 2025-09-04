# src/api/v1/__init__.py
from fastapi import APIRouter

from .get_forecast import router as func_get_forecast_data
from .get_sensor_id_list import router as func_get_sensor_id_list
from .get_mini_charts_data import router as func_get_mini_charts_data
from .create_notification import router as create_alert
from .delete_notification import router as delete_alert
from .list_notifications import router as notifications_list
from .generate_forecast import router as func_generate_forecast
from .get_possible_date import router as func_generate_possible_date
from .get_accuracy_by_period import router as func_metrix_by_period
from .get_possible_date_for_metrix import router as func_fetch_possible_date_for_metrix
from src.auth_proxi.authorization import router as proxy_auth_router
from src.auth_proxi.register_org import router as register_org_and_superuser
from src.auth_proxi.register_user import router as register_user_router
from src.auth_proxi.change_user_status import router as change_user_status


router = APIRouter()

router.include_router(proxy_auth_router, prefix="/auth", tags=["Auth users"])
router.include_router(register_org_and_superuser, prefix="/register", tags=["Register Organization and Superuser"])
router.include_router(register_user_router, prefix="/register", tags=["Register User in Organization"])
router.include_router(change_user_status, prefix="/register", tags=["Change User Status in Organization"])

router.include_router(func_get_forecast_data, tags=["Scheduled Forecasting"])
router.include_router(func_get_sensor_id_list, tags=["Scheduled Forecasting"])
router.include_router(func_metrix_by_period, tags=["Scheduled Forecasting"])
router.include_router(func_fetch_possible_date_for_metrix, tags=["Scheduled Forecasting"])

router.include_router(func_get_mini_charts_data, tags=["Get Mini Charts Data"])

router.include_router(create_alert, tags=["Notifications Area"])
router.include_router(notifications_list, tags=["Notifications Area"])
router.include_router(delete_alert, tags=["Notifications Area"])

router.include_router(func_generate_forecast, tags=["Generate Forecast Area"])
router.include_router(func_generate_possible_date, tags=["Generate Forecast Area"])
