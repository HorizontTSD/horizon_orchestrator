from fastapi import APIRouter, HTTPException, Request, Depends, Query
from src.schemas import GenerateDateResponse, MetricsResponse
from src.security.check_token import access_token_validator
from environs import Env
from src.schedule_forecast_proxi.proxi import _forward_request


env = Env()
env.read_env()
forecast_service_url = env.str("SCHEDULE_FORECAST_SERVICE", "http://0.0.0.0:7070")
forecast_api_url = forecast_service_url + "/schedule_forecast/api/v1/metrics"

router = APIRouter(prefix="/metrics")


@router.get("/get_possible_date_for_metrics", response_model=GenerateDateResponse, summary="Возвращает возможные даты для замера точности модели")
async def proxy_get_possible_date_for_metrix(
        data_name: str = Query(..., description="Название данных для метрик"),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт возвращает возможные даты для замера точности модели.

    Description:
    - Требуется действующий access_token
    - Проверяет право 'metrics.view'

    Parameters:
    - **data_name** (str, query): Название данных для метрик. можно получить из - **orchestrator/api/v1/schedule_forecast/list**

    Raises:
    - **HTTPException 403**: Если пользователь не имеет права 'metrics.view'
    - **HTTPException 500**: Если произошла ошибка при получении данных
    """
    headers = {"authorization": request.headers["authorization"]}
    params = {"data_name": data_name}
    return await _forward_request(
        method="GET",
        endpoint=f"{forecast_api_url}/get_possible_date_for_metrics",
        params=params,
        headers=headers
    )


@router.get("/get_metrics_by_date", response_model=MetricsResponse, summary="Возвращает метрики прогноза по датам")
async def proxy_get_metrics_by_date(
        data_name: str = Query(..., description="Название данных для метрик"),
        start_date: str = Query(..., description="Начальная дата"),
        end_date: str = Query(..., description="Конечная дата"),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт возвращает метрики прогноза по указанным датам.

    Description:
    - Требуется действующий access_token
    - Проверяет право 'metrics.view'
    - **data_name** можно получить из orchestrator/api/v1/schedule_forecast/list
    - **start_date** и **end_date** можно получить из orchestrator/api/v1/metrics/get_possible_date_for_metrics

    Пример запроса:
        GET /schedule_forecast/api/v1/metrix/get_metrics_by_date?data_name=example_data_name&start_date=2025-09-01&end_date=2025-09-12

    Parameters:
    - **data_name** (str, query): Название данных для метрик
    - **start_date** (str, query): Начальная дата
    - **end_date** (str, query): Конечная дата

    Raises:
    - **HTTPException 403**: Если пользователь не имеет права 'metrics.view'
    - **HTTPException 500**: Если произошла ошибка при получении данных
    """
    headers = {"authorization": request.headers["authorization"]}
    params = {"data_name": data_name, "start_date": start_date, "end_date": end_date}
    return await _forward_request(
        method="GET",
        endpoint=f"{forecast_api_url}/get_metrics_by_date",
        params=params,
        headers=headers
    )
