from fastapi import APIRouter

from .v1.get_forecast import router as func_get_forecast_data
from .v1.get_sensor_id_list import router as func_get_sensor_id_list
from .v1.get_mini_charts_data import router as func_get_mini_charts_data
from .v1.create_notification import router as create_alert
from .v1.delete_notification import router as delete_alert
from .v1.list_notifications import router as notifications_list
from .v1.generate_forecast import router as func_generate_forecast
from .v1.get_possible_date import router as func_generate_possible_date
from .v1.get_accuracy_by_period import router as func_metrix_by_period
from .v1.get_possible_date_for_metrix import router as func_fetch_possible_date_for_metrix
from src.auth_proxi.authorization import router as proxy_auth_router
from src.auth_proxi.register_org import router as register_org_and_superuser
from src.auth_proxi.register_user import router as register_user_router
from src.auth_proxi.change_user_status import router as change_user_status

from src.schedule_forecast_proxi.dbconnection_endpoints import router as dbconnection_endpoints
from src.schedule_forecast_proxi.metrics_endpoints import router as metrics_endpoints
from src.schedule_forecast_proxi.set_forecast_enpoints import router as set_forecast_enpoints


api_router = APIRouter()

api_router.include_router(proxy_auth_router, prefix="/auth", tags=["Auth users"])
api_router.include_router(register_org_and_superuser, prefix="/register", tags=["Register Organization and Superuser"])
api_router.include_router(register_user_router, prefix="/register", tags=["Register User in Organization"])
api_router.include_router(change_user_status, prefix="/register", tags=["Change User Status in Organization"])

api_router.include_router(func_get_forecast_data, tags=["Scheduled Forecasting"])
api_router.include_router(func_get_sensor_id_list, tags=["Scheduled Forecasting"])
api_router.include_router(func_metrix_by_period, tags=["Scheduled Forecasting"])
api_router.include_router(func_fetch_possible_date_for_metrix, tags=["Scheduled Forecasting"])

api_router.include_router(func_get_mini_charts_data, tags=["Get Mini Charts Data"])

api_router.include_router(create_alert, tags=["Notifications Area"])
api_router.include_router(notifications_list, tags=["Notifications Area"])
api_router.include_router(delete_alert, tags=["Notifications Area"])

api_router.include_router(func_generate_forecast, tags=["Generate Forecast Area"])
api_router.include_router(func_generate_possible_date, tags=["Generate Forecast Area"])

api_router.include_router(dbconnection_endpoints, tags=["DB Connection Area"])
api_router.include_router(set_forecast_enpoints, tags=["Schedule Forecast Area"])
api_router.include_router(metrics_endpoints, tags=["Metrics Schedule Forecast Area"])




