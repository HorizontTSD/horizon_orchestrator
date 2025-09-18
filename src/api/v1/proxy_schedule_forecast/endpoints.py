# src/api/v1/proxy_schedule_forecast/endpoints.py
from fastapi import APIRouter, Depends, Query, Body 
from src.core.token import token_validator
from src.services.proxy_schedule_forecast_service import (
    proxy_create_forecast_config,
    proxy_list_forecast_configs,
    proxy_delete_forecast_config,
    proxy_get_forecast_methods,
    proxy_get_forecast_data,
)

import httpx
from fastapi import HTTPException, status
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


router = APIRouter(prefix="/schedule_forecast", tags=["Proxy Schedule Forecast Config"])

@router.get("/forecast_methods") 
async def get_forecast_methods(token: str = Depends(token_validator)):
    response = await proxy_get_forecast_methods(token)
    return await handle_proxy_response(response)

@router.get("/list") 
async def list_forecasts(token: str = Depends(token_validator)):
    response = await proxy_list_forecast_configs(token)
    return await handle_proxy_response(response)

@router.post("/create") 
async def create_forecast(payload: dict = Body(...), token: str = Depends(token_validator)):
     response = await proxy_create_forecast_config(token, payload)
     return await handle_proxy_response(response)

@router.delete("/delete/{forecast_id}") 
async def delete_forecast(forecast_id: int, token: str = Depends(token_validator)):
     response = await proxy_delete_forecast_config(token, forecast_id)
     return await handle_proxy_response(response)

@router.get("/get_forecast_data") 
async def get_forecast_data_endpoint(
    data_name: str = Query(...), token: str = Depends(token_validator)
):
     response = await proxy_get_forecast_data(token, data_name)
     return await handle_proxy_response(response)
