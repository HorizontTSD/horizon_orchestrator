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



router = APIRouter()

router.include_router(func_get_forecast_data, tags=["Get Forecast Data"])
router.include_router(func_get_mini_charts_data, tags=["Get Mini Charts Data"])
router.include_router(func_get_sensor_id_list, tags=["Get Sensor ID List"])
router.include_router(create_alert, tags=["Create Notifications"])
router.include_router(notifications_list, tags=["Notifications List"])
router.include_router(delete_alert, tags=["Delete Notifications"])
router.include_router(func_generate_forecast, tags=["Generate Forecast"])
router.include_router(func_generate_possible_date, tags=["Get Possible Date"])
router.include_router(func_metrix_by_period, tags=["Get Accuracy Predict Metrix by Period"])
router.include_router(func_fetch_possible_date_for_metrix, tags=["Get Possible Date For Metrix by Period"])
