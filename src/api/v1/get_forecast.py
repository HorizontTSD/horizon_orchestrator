# src/api/v1/greeting.py
from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Depends
from src.schemas import ForecastData
from src.services.data_fetcher_service import data_fetcher
from src.security.check_token import access_token_validator
from src.core.logger import logger
from src.security.permissions import check_permission


router = APIRouter()


@router.post("/get_forecast_data")
async def func_get_forecast_data(body: Annotated[
    ForecastData, Body(
        example={
            "sensor_ids": ["arithmetic_1464947681"]
        })],
        user_info=Depends(access_token_validator)
):
    """
    Возвращает данные о датчиках в структурированном формате.

    Формат возвращаемых данных:
    {
        "sensor_1": data,
        "sensor_2": data,
        ...
    }

    Где "data" содержит следующие ключи:

    1. **description** (описание датчика):
        - "sensor_name" (str) — отображаемое имя датчика на фронте.
        - "sensor_id" (str) — отображаемый ID датчика на фронте.

    2. **map_data** (данные для визуализации):
        - "data" (dict) — данные для отрисовки графиков:
            - "last_real_data" — последние известные реальные данные из БД.
            - "actual_prediction_lstm" — актуальный прогноз модели LSTM.
            - "actual_prediction_xgboost" — актуальный прогноз модели XGBoost.
            - "ensemble" — актуальный прогноз модели Ensemble.
        - "last_know_data" (str) — последняя известная дата в БД реальных данных.
        - "legend" (dict) — легенда к графику:
            - "last_know_data_line" (dict) — линия последней известной даты, разделяет график на "Реальные данные" и "Прогноз":
                - "text" (dict):
                    - "en" — английский текст.
                    - "ru" — русский текст.
                - "color" (str) — цвет линии.
            - "real_data_line" (dict) — линия реальных данных:
                - "text" (dict):
                    - "en" — английский текст.
                    - "ru" — русский текст.
                - "color" (str) — цвет линии.
            - "LSTM_data_line" (dict) — линия прогноза LSTM:
                - "text" (dict):
                    - "en" — английский текст.
                    - "ru" — русский текст.
                - "color" (str) — цвет линии.
            - "XGBoost_data_line" (dict) — линия прогноза XGBoost:
                - "text" (dict):
                    - "en" — английский текст.
                    - "ru" — русский текст.
                - "color" (str) — цвет линии.
            - "Ensemble_data_line" (dict) — линия прогноза Ensemble:
                - "text" (dict):
                    - "en" — английский текст.
                    - "ru" — русский текст.
                - "color" (str) — цвет линии.

    3. **table_to_download** (таблица прогноза) — таблица данных, доступная для скачивания пользователем.

    4. **metrix_tables** (метрики моделей за последние сутки):
        - "XGBoost" (dict) — метрики для модели XGBoost:
            - "metrics_table" (dict):
                - "text" (dict):
                    - "en" — английский текст подписи.
                    - "ru" — русский текст подписи.
        - "LSTM" (dict) — метрики для модели LSTM:
            - "metrics_table" (dict):
                - "text" (dict):
                    - "en" — английский текст подписи.
                    - "ru" — русский текст подписи.
    """
    check_permission(user_info=user_info, permission="dashboard.view")

    try:
        sensor_ids = body.sensor_ids
        response = await data_fetcher(sensor_ids)

        return response

    except Exception as ApplicationError:
        logger.error(ApplicationError.__repr__())
        raise HTTPException(
            status_code=400,
            detail="Unknown Error",
            headers={"X-Error": f"{ApplicationError.__repr__()}"},
        )
