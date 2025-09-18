from fastapi import APIRouter, HTTPException, Body, Path, Request, Depends
from src.schemas import (
    CreateDBConnectionResponse, CreateDBConnectionRequest,
    DeleteDBConnectionResponse, DBConnectionListResponse,
    TablesListResponse, ColumnsListResponse
)
from src.security.check_token import access_token_validator
from environs import Env
from src.schedule_forecast_proxi.proxi import _forward_request

env = Env()
env.read_env()
url = env.str("SCHEDULE_FORECAST_SERVICE", "http://0.0.0.0:7070")
schedule_forecast_url = url + "/schedule_forecast/api/v1"


router = APIRouter(prefix="/db_connection")


@router.post("/create", response_model=CreateDBConnectionResponse, summary="Get organization's users")
async def proxy_create_dbconnection(
        payload: CreateDBConnectionRequest = Body(..., example={
            "connection_schema": "PostgreSQL",
            "connection_name": "Тестовое соеденение",
            "db_name": "my_database",
            "host": "localhost",
            "port": 5432,
            "ssl": True,
            "db_user": "postgres",
            "db_password": "password123"
        }),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для создания соединения с базой данных организации.

    Description:
    - Создает новое соединение с указанной базой данных
    - Проверяет роль пользователя (только admin или superuser)
    - Проверяет наличие права 'connection.create'
    - Возвращает подтверждение успешного подключения или текст ошибки

    Parameters:
    - **payload** (CreateDBConnectionRequest, body): Параметры подключения к БД

    Raises:
    - **HTTPException 403**: Если пользователь не имеет роли или права на создание соединения
    - **HTTPException 500**: Если произошла ошибка при создании соединения
    """
    headers = {"authorization": request.headers["authorization"], "Content-Type": "application/json"}
    return await _forward_request(
        method="POST",
        endpoint=f"{schedule_forecast_url}/db_connection/create",
        payload=payload.dict(),
        headers=headers
    )


@router.delete("/delete/{connection_id}", response_model=DeleteDBConnectionResponse, summary="Удаление соединения организации")
async def proxy_delete_dbconnection(
        connection_id: int = Path(..., description="ID соединения для удаления"),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для логического удаления соединения с базой данных организации.

    Description:
    - Проверяет роль пользователя (только admin или superuser)
    - Проверяет наличие права 'connection.delete'
    - Устанавливает флаг is_deleted=True для соединения
    - Проверяет, что соединение принадлежит организации пользователя

    Parameters:
    - **connection_id** (int, path): ID соединения

    Raises:
    - **HTTPException 403**: Если пользователь не имеет роли или права на удаление
    - **HTTPException 404**: Если соединение не найдено или уже удалено
    - **HTTPException 500**: Если произошла ошибка при удалении
    """
    headers = {"authorization": request.headers["authorization"], "Content-Type": "application/json"}
    return await _forward_request("DELETE", f"{schedule_forecast_url}/db_connection/delete/{connection_id}", headers=headers)


@router.get("/list", response_model=DBConnectionListResponse, summary="Получение списка соединений организации")
async def proxy_list_dbconnections(
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для получения списка соединений организации.

    Description:
    - Проверяет роль пользователя (admin или superuser)
    - Проверяет наличие права 'connection.view'
    - Возвращает список соединений для организации пользователя

    Raises:
    - **HTTPException 403**: Если пользователь не имеет роли или права на просмотр
    - **HTTPException 404**: Если соединения не найдены
    - **HTTPException 500**: Если произошла ошибка при получении списка
    """
    headers = {"authorization": request.headers["authorization"]}
    return await _forward_request(
        method="GET",
        endpoint=f"{schedule_forecast_url}/db_connection/list",
        headers=headers
    )


@router.get("/{connection_id}/tables", response_model=TablesListResponse, summary="Получение списка таблиц соединения")
async def proxy_get_connection_tables(
        connection_id: int = Path(..., description="ID соединения"),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для получения списка таблиц по соединению организации.

    - Проверяет роль пользователя (admin или superuser)
    - Проверяет наличие права 'connection.view'
    - Проверяет, что соединение принадлежит организации пользователя
    - Возвращает список таблиц соединения

    Raises:
    - HTTPException 403: если пользователь не имеет роли или права на просмотр
    - HTTPException 404: если соединение не найдено
    - HTTPException 500: если произошла ошибка при получении таблиц
    """
    headers = {"authorization": request.headers["authorization"]}
    return await _forward_request(
        method="GET",
        endpoint=f"{schedule_forecast_url}/db_connection/{connection_id}/tables",
        headers=headers
    )


@router.get("/{connection_id}/{table_name}/columns", response_model=ColumnsListResponse, summary="Получение списка колонок таблицы соединения")
async def proxy_get_connection_table_columns(
        connection_id: int = Path(..., description="ID соединения"),
        table_name: str = Path(..., description="Название таблицы"),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для получения списка колонок таблицы по соединению организации.

    - Проверяет роль пользователя (admin или superuser)
    - Проверяет наличие права 'connection.view'
    - Проверяет, что соединение принадлежит организации пользователя
    - Возвращает список колонок таблицы соединения

    Raises:
    - HTTPException 403: если пользователь не имеет роли или права на просмотр
    - HTTPException 404: если соединение или таблица не найдены
    - HTTPException 500: если произошла ошибка при получении колонок
    """
    headers = {"authorization": request.headers["authorization"]}
    return await _forward_request(
        method="GET",
        endpoint=f"{schedule_forecast_url}/db_connection/{connection_id}/{table_name}/columns",
        headers=headers
    )
