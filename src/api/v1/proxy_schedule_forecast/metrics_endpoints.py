# src/api/v1/proxy_schedule_forecast/metrics_endpoints.py
from fastapi import APIRouter, Depends, Query, HTTPException, status
from src.core.token import token_validator
from src.services.proxy_schedule_forecast_service import (
    proxy_get_possible_date_for_metrix,
    proxy_get_metrics_by_date
)
from src.model import ProxyError

router = APIRouter(prefix="/metrix", tags=["Proxy Schedule Forecast Metrics"])

@router.get("/get_possible_date_for_metrix", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_get_possible_date_for_metrix_endpoint(
    data_name: str = Query(...),
    token: str = Depends(token_validator)
):
    response = await proxy_get_possible_date_for_metrix(token, data_name)
    return await handle_proxy_response(response)

@router.get("/get_metrics_by_date", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_get_metrics_by_date_endpoint(
    data_name: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    token: str = Depends(token_validator)
):
    response = await proxy_get_metrics_by_date(token, data_name, start_date, end_date)
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
