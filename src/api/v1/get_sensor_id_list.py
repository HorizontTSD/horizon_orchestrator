# src/api/v1/greeting.py
from fastapi import APIRouter, Body, HTTPException
from src.core.logger import logger
from src.services.sensor_list_fetcher_service import get_sensor_list

router = APIRouter()

@router.get("/get_sensor_id_list")
async def func_get_sensor_id_list():
    """
    Возвращает список доступных датчиков.

    Формат ответа:
    [
        "sensor_id_1",
        "sensor_id_2",
        ...
    ]

    Каждый элемент списка — это строка с идентификатором доступного датчика.
    """
    try:
        response = await get_sensor_list()
        return response

    except Exception as ApplicationError:
        logger.error(ApplicationError.__repr__())
        raise HTTPException(
            status_code=400,
            detail="Unknown Error",
            headers={"X-Error": f"{ApplicationError.__repr__()}"},
        )