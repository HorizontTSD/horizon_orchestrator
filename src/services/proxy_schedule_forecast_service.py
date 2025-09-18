# src/services/proxy_schedule_forecast_service.py
import httpx
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from src.core.configuration.config import settings
from src.core.logger import logger

SCHEDULE_FORECAST_SERVICE_URL = f"{settings.SET_SCHEDULE_FORECAST_HORIZON_URL.rstrip('/')}" 

async def proxy_request(
    method: str,
    path: str,
    token: str,
    json_data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> httpx.Response:
    """
    Выполняет HTTP-запрос к микросервису set_schedule_forecast_horizon.
    """

    if not path.startswith('/'):
        path = '/' + path
    url = f"{SCHEDULE_FORECAST_SERVICE_URL}{path}"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            logger.debug(f"Proxying {method} request to {url}")
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                params=params
            )
            logger.debug(f"Received response from {url}: {response.status_code}")
            return response
        except httpx.RequestError as e:
            logger.error(f"Request error while proxying to {url}: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service Unavailable",
                headers={"X-Error": "Failed to connect to the schedule forecast service"}
            )
        except Exception as e:
            logger.error(f"Unexpected error while proxying to {url}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
                headers={"X-Error": "An error occurred while proxying the request"}
            )

# DB Connection Endpoints
async def proxy_create_dbconnection(token: str, payload: Dict[str, Any]) -> httpx.Response:
    return await proxy_request("POST", "/api/v1/db_connection/create", token, json_data=payload)

async def proxy_delete_dbconnection(token: str, connection_id: int) -> httpx.Response:
    return await proxy_request("DELETE", f"/api/v1/db_connection/delete/{connection_id}", token)

async def proxy_list_dbconnections(token: str) -> httpx.Response:
    return await proxy_request("GET", "/api/v1/db_connection/list", token)

async def proxy_get_connection_tables(token: str, connection_id: int) -> httpx.Response:
    return await proxy_request("GET", f"/api/v1/db_connection/{connection_id}/tables", token)

async def proxy_get_connection_table_columns(token: str, connection_id: int, table_name: str) -> httpx.Response:
    return await proxy_request("GET", f"/api/v1/db_connection/{connection_id}/{table_name}/columns", token)

# Schedule Forecast Endpoints
async def proxy_get_forecast_methods(token: str) -> httpx.Response:
    return await proxy_request("GET", "/api/v1/schedule_forecast/forecast_methods", token)

async def proxy_create_forecast_config(token: str, payload: Dict[str, Any]) -> httpx.Response:
    return await proxy_request("POST", "/api/v1/schedule_forecast/create", token, json_data=payload)

async def proxy_list_forecast_configs(token: str) -> httpx.Response:
    return await proxy_request("GET", "/api/v1/schedule_forecast/list", token)

async def proxy_delete_forecast_config(token: str, forecast_id: int) -> httpx.Response:
    return await proxy_request("DELETE", f"/api/v1/schedule_forecast/delete/{forecast_id}", token)

async def proxy_get_forecast_data(token: str, data_name: str) -> httpx.Response:
    """Проксирует запрос на получение данных прогноза."""
    params = {"data_name": data_name}
    return await proxy_request("GET", "/api/v1/schedule_forecast/get_forecast_data", token, params=params)

# Metrics Endpoints
async def proxy_get_possible_date_for_metrix(token: str, data_name: str) -> httpx.Response:
    """Проксирует запрос на получение возможных дат для метрик."""
    params = {"data_name": data_name}
    return await proxy_request("GET", "/api/v1/metrix/get_possible_date_for_metrix", token, params=params)

async def proxy_get_metrics_by_date(token: str, data_name: str, start_date: str, end_date: str) -> httpx.Response:
    """Проксирует запрос на получение метрик по датам."""
    params = {
        "data_name": data_name,
        "start_date": start_date,
        "end_date": end_date
    }
    return await proxy_request("GET", "/api/v1/metrix/get_metrics_by_date", token, params=params)


async def proxy_get_tables_info(token: str) -> httpx.Response:
    return await proxy_request("GET", "/api/v1/tables-info/", token) 
