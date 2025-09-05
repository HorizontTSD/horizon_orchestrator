# src/api/v1/greeting.py
from fastapi import APIRouter, Body, HTTPException, Depends
from src.core.logger import logger
from src.services.accuracy_by_period_service import fetch_possible_date_for_metrix
from src.schemas import PossibleData
from typing import Annotated
from src.auth_proxi.check_token import access_token_validator



router = APIRouter()

@router.post("/fetch_possible_date_for_metrix")
async def func_fetch_possible_date_for_metrix(body: Annotated[
    PossibleData, Body(
        example={
            "sensor_ids": ["arithmetic_1464947681"]
        })],
        _=Depends(access_token_validator)
):

    """
    Асинхронная функция для получения возможных дат для метрик для каждого сенсора.

    Для каждого сенсора функция извлекает минимальные и максимальные даты из таблиц
    предсказаний для LSTM и XGBoost, а также определяет дату начала по умолчанию
    (за один день до максимальной даты) и возвращает эти данные.

    Формат возвращаемых данных:
    {
        sensor_id (str): {
            "earliest_date": (datetime) — самая ранняя дата среди предсказаний для LSTM и XGBoost,
            "max_date": (datetime) — максимальная дата в таблице сенсора,
            "start_default_date": (datetime) — дата начала по умолчанию (максимальная дата - 1 день),
            "end_default_date": (datetime) — дата конца по умолчанию (максимальная дата),
        }
        ...
    }

    Параметры:
    sensor_ids (list) — список идентификаторов сенсоров, для которых нужно получить данные.

    Возвращаемое значение:
    dict — словарь с данными по каждому сенсору.

    Исключения:
    - Может возникнуть исключение, если соединение с базой данных не удастся.
    """


    try:
        sensor_ids = body.sensor_ids
        response = await fetch_possible_date_for_metrix(sensor_ids)
        return response

    except Exception as ApplicationError:
        logger.error(ApplicationError.__repr__())
        raise HTTPException(
            status_code=400,
            detail="Unknown Error",
            headers={"X-Error": f"{ApplicationError.__repr__()}"},
        )