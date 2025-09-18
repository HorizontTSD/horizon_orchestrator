from fastapi import APIRouter, HTTPException, Body, Path, Request, Depends, Query
from src.schemas import (
    ForecastConfigRequest, ForecastConfigResponse,
    ScheduleForecastingResponse, DeleteForecastResponse
)
from src.security.check_token import access_token_validator
from environs import Env
from src.schedule_forecast_proxi.proxi import _forward_request


env = Env()
env.read_env()
forecast_service_url = env.str("SCHEDULE_FORECAST_SERVICE", "http://0.0.0.0:7070")
forecast_api_url = forecast_service_url + "/schedule_forecast/api/v1/schedule_forecast"

router = APIRouter(prefix="/schedule_forecast")


@router.get("/forecast_methods", summary="Возвращает список возможных методов прогноза")
async def proxy_get_forecast_methods_list(request: Request, _=Depends(access_token_validator)):
    """
    Эндпоинт возвращает список возможных методов прогнозирования.

    Description:
    - Требуется действующий access_token
    - Проверяет право 'schedule_forecast.create'

    Raises:
    - **HTTPException 403**: Если пользователь не имеет права 'schedule_forecast.create'
    - **HTTPException 500**: Если произошла ошибка при получении данных
    """
    headers = {"authorization": request.headers["authorization"]}
    return await _forward_request("GET", f"{forecast_api_url}/forecast_methods", headers=headers)


@router.post("/create", response_model=ForecastConfigResponse, summary="Создание настройки прогнозирования")
async def proxy_create_forecast_config(
        payload: ForecastConfigRequest = Body(...),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для создания настройки прогнозирования.

    Description:
    - Сохраняет параметры прогнозирования для указанной таблицы
    - Проверяет роль пользователя (только admin или superuser)
    - Проверяет наличие права 'forecast.create'
    - Возвращает подтверждение успешного создания или текст ошибки

    - **connection_id** - Можно получить из - **orchestrator/api/v1/schedule_forecast/forecast_methods**
    - **data_name** - Задать название своим данным **самостоятельно**
    - **source_table** - Можно получить из - **orchestrator/api/v1/db_connection/{connection_id}/tables**
    - **time_column** - Можно получить и выбрать из - **orchestrator/api/v1/db_connection/{connection_id}/{table_name}/columns**
    - **target_column** - Можно получить и выбрать из - **orchestrator/api/v1/db_connection/{connection_id}/{table_name}/columns**
    - **count_time_points_predict** - Задать сколько точек прогнозировать, **к примеру 100**
    - **target_db**  - указать либо **self_host** - что означает хранение прошгноза на стороне кто его запрашивает, либо любое другое, что будет обозначать хранение у нас
    - **methods** - Можно получить из -

    Raises:
    - **HTTPException 403**: Если пользователь не имеет роли или права
    - **HTTPException 500**: Если произошла ошибка при сохранении настройки
    """
    headers = {"authorization": request.headers["authorization"]}
    return await _forward_request("POST", f"{forecast_api_url}/create", payload=payload.dict(), headers=headers)


@router.get("/list", response_model=list[ScheduleForecastingResponse], summary="Получение списка настроек прогнозирования")
async def proxy_get_forecast_configs(request: Request, _=Depends(access_token_validator)):
    """
    Эндпоинт для получения списка настроек прогнозирования.

    Description:
    - Возвращает все настройки прогнозирования для организации пользователя
    - Проверяет роль пользователя (только admin или superuser)
    - Проверяет наличие права 'forecast.view'
    - Возвращает список настроек или текст ошибки

    Raises:
    - **HTTPException 403**: Если пользователь не имеет роли или права
    - **HTTPException 404**: Если настройки не найдены
    - **HTTPException 500**: Если произошла ошибка при получении данных
    """
    headers = {"authorization": request.headers["authorization"]}
    return await _forward_request(
        method="GET",
        endpoint=f"{forecast_api_url}/list",
        headers=headers
    )


@router.delete("/delete/{forecast_id}", response_model=DeleteForecastResponse, summary="Удаление настройки прогноза")
async def proxy_delete_forecast(
        forecast_id: int = Path(..., description="ID настройки прогноза для удаления"),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для удаления настройки прогнозирования.

    Description:
    - Проверяет роль пользователя (только admin или superuser)
    - Проверяет наличие права 'schedule_forecast.delete'
    - Удаляет настройку прогнозирования для организации
    - **forecast_id** - Можно получить из - **orchestrator/api/v1/schedule_forecast/list**


    Raises:
    - **HTTPException 403**: Если пользователь не имеет роли или права
    - **HTTPException 500**: Если произошла ошибка при удалении
    """
    headers = {"authorization": request.headers["authorization"]}
    return await _forward_request(
        method="DELETE",
        endpoint=f"{forecast_api_url}/delete/{forecast_id}",
        headers=headers)


@router.get("/get_forecast_data", summary="Возвращает данные о датчиках в структурированном формате")
async def proxy_get_forecast_data(
        data_name: str = Query(..., description="Название данных"),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт возвращает данные о датчиках в структурированном формате.

    Description:
    - Требуется действующий access_token
    - Проверяет право 'dashboard.view'
    - **data_name** можно получить из метода api/v1/schedule_forecast/list

    Формат возвращаемых данных подробно описан в исходном коде.

    Raises:
    - **HTTPException 403**: Если пользователь не имеет права 'dashboard.view'
    - **HTTPException 500**: Если произошла ошибка при получении данных
    """
    headers = {"authorization": request.headers["authorization"]}
    params = {"data_name": data_name}
    return await _forward_request(
        method="GET",
        endpoint=f"{forecast_api_url}/get_forecast_data",
        params=params,
        headers=headers
    )
