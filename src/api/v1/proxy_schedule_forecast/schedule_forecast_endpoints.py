# src/api/v1/proxy_schedule_forecast/schedule_forecast_endpoints.py
from fastapi import APIRouter, Depends, Body, Path, Query, HTTPException, status
from src.core.token import token_validator
from src.services.proxy_schedule_forecast_service import (
    proxy_create_forecast_config,
    proxy_list_forecast_configs,
    proxy_delete_forecast_config,
    proxy_get_forecast_methods,
    proxy_get_forecast_data,
)
from src.model import ProxyError

router = APIRouter(prefix="/schedule_forecast", tags=["Proxy Schedule Forecast Config"])

@router.get("/forecast_methods", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_get_forecast_methods_endpoint(token: str = Depends(token_validator)):
    response = await proxy_get_forecast_methods(token)
    return await handle_proxy_response(response)

@router.post("/create", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_create_forecast_config_endpoint(
    payload: dict = Body(...),
    token: str = Depends(token_validator)
):
     response = await proxy_create_forecast_config(token, payload)
     return await handle_proxy_response(response)

@router.get("/list", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_list_forecast_configs_endpoint(token: str = Depends(token_validator)):
    response = await proxy_list_forecast_configs(token)
    return await handle_proxy_response(response)

@router.delete("/delete/{forecast_id}", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_delete_forecast_config_endpoint(
    forecast_id: int = Path(...),
    token: str = Depends(token_validator)
):
    response = await proxy_delete_forecast_config(token, forecast_id)
    return await handle_proxy_response(response)

@router.get("/get_forecast_data", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_get_forecast_data_endpoint(
    data_name: str = Query(...),
    token: str = Depends(token_validator)
):
    response = await proxy_get_forecast_data(token, data_name)
    return await handle_proxy_response(response)

@router.get("/get_forecast_data", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_get_forecast_data_endpoint(
    data_name: str = Query(..., description="Имя конфигурации прогноза (data_name)"),
    token: str = Depends(token_validator)
):
    """
    Проксирует запрос на получение данных прогноза для построения графика.
    """
    response = await proxy_get_forecast_data(token, data_name)
    return await handle_proxy_response(response)

# Вспомогательная функция для обработки ответа
async def handle_proxy_response(response: httpx.Response):
    try:
        try:
            data = response.json()
        except:
            data = response.text

        if 200 <= response.status_code < 300:
             return data
        else:
            raise HTTPException(status_code=response.status_code, detail=data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
