from environs import Env
from fastapi import APIRouter, HTTPException, Depends, Request, status
import httpx
from src.schemas import DataNameListResponse
from src.security.check_token import access_token_validator
from src.security.permissions import check_permission

env = Env()
env.read_env()

schedule_forecast_service_url = env.str("SCHEDULE_FORECAST_SERVICE", "http://localhost:7070")

router = APIRouter()

@router.get(
    "/data_name_list",
    response_model=DataNameListResponse,
    status_code=status.HTTP_200_OK,
    summary="Получение списка настроек прогнозирования (прокси)"
)
async def proxy_get_forecast_configs(
        request: Request,
        user_info = Depends(access_token_validator)
):

    check_permission(user_info=user_info, permission="dashboard.view")

    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{schedule_forecast_service_url}/set_schedule_forecast/api/v1/schedule_forecast/list",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            data_names = [item["data_name"] for item in data if "data_name" in item]
            return DataNameListResponse(data_names=data_names)
        except httpx.HTTPStatusError as exc:
            try:
                detail = exc.response.json().get("detail", exc.response.text)
            except ValueError:
                detail = exc.response.text
            raise HTTPException(status_code=exc.response.status_code, detail=detail)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Schedule forecast service unavailable: {str(exc)}")
