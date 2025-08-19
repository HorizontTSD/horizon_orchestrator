# src/api/v1/greeting.py
from fastapi import APIRouter, Body, HTTPException
from src.core.logger import logger
from src.services.accuracy_by_period_service import calc_accuracy_by_period
from src.schemas import MetrixByPeriod
from typing import Annotated


router = APIRouter()

@router.post("/accuracy_by_period")
async def func_metrix_by_period(body: Annotated[
    MetrixByPeriod, Body(
        example={
            "sensor_ids": ["arithmetic_1464947681"],
            "date_start": "2025-07-12 10:37:00",
            "date_end": "2025-07-13 10:32:00"
        })]):
    """
    Вычисляет метрики точности прогноза за указанный период времени.

    - **sensor_ids**: список идентификаторов сенсоров
    - **date_start**: начало периода в формате `YYYY-MM-DD HH:MM:SS`
    - **date_end**: конец периода в формате `YYYY-MM-DD HH:MM:SS`

    Возвращает словарь с рассчитанными метриками (MAE, RMSE, MAPE и др.) для каждого сенсора.
    Используется для оценки качества предсказаний модели и анализа её производительности.
    """

    try:
        sensor_ids = body.sensor_ids
        date_start = body.date_start
        date_end = body.date_end

        response = await calc_accuracy_by_period(sensor_ids, date_start, date_end)
        return response

    except Exception as ApplicationError:
        logger.error(ApplicationError.__repr__())
        raise HTTPException(
            status_code=400,
            detail="Unknown Error",
            headers={"X-Error": f"{ApplicationError.__repr__()}"},
        )
