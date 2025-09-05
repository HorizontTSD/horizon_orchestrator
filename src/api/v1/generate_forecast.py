import os
import pandas as pd
from fastapi import APIRouter, Body, HTTPException, Depends
from src.core.logger import logger
from typing import Annotated
from src.schemas import PredictRequest
from src.services.tool_backend_service import proxy_generate_forecast
from src.security.check_token import access_token_validator
from src.security.permissions import check_permission


home_path = os.getcwd()


router = APIRouter()

example_df = pd.read_csv(f'{home_path}/src/examples/example_data.csv')
example_df_long = example_df.iloc[:1000]

example_df_json_long = example_df_long.to_dict(orient="records")


@router.post("/generate_forecast")
async def func_generate_forecast(body: Annotated[
    PredictRequest, Body(
        example={
            "df": example_df_json_long,
            "time_column": "time",
            "col_target": "load_consumption",
            "forecast_horizon_time": "2022-09-10 05:55:00"
        })],
        user_info=Depends(access_token_validator)
):

    """
    Генерирует прогноз временного ряда на основе исторических данных.

    Описание:
    ----------
    Функция принимает временной ряд, нормализует данные, формирует будущий интервал времени и
    выполняет прогнозирование. Возвращает результат в формате JSON, который включает последние известные
    данные и прогнозируемые значения для визуализации на фронтенде.

    Параметры:
    ----------
    1. `df` (pd.DataFrame) — Исходный DataFrame, содержащий временной ряд с целевой переменной.
    2. `time_column` (str) — Название столбца, содержащего временные метки.
    3. `col_target` (str) — Название целевой переменной, по которой строится прогноз.
    4. `forecast_horizon_time` (str) — Временная граница прогнозирования (последняя возможная дата прогноза).
    5. `lag` (int, optional, по умолчанию 4) — Количество временных лагов, используемых для предсказания.
    6. `forecast_type` (str, optional, по умолчанию 'predictions') — Тип прогнозирования, определяющий, какие предсказания будут сгенерированы.
    7. `norm_values` (bool, optional, по умолчанию True) — Флаг нормализации значений перед подачей в модель.

    Возвращает:
    ----------
    1. `map_data` (dict) - словапь данных для отрисовки
        - **data** (dict):
            - **last_real_data** (list[dict]) — Последние известны еданные пользователя
            - **predictions** (list[dict]) — Данные предсказания.

    2. `last_know_data_line` (dict) — линия, обозначающая последнюю известную дату:
        - **text** (dict):
            - **en** (str) — описание на английском языке.
            - **ru** (str) — описание на русском языке.
        - **color** (str) — цвет линии, разделяющей реальные данные и прогноз.
    3. `real_data_line` (dict) — линия реальных данных:
        - **text** (dict):
            - **en** (str) — описание на английском языке.
            - **ru** (str) — описание на русском языке.
        - **color** (str) — цвет линии реальных данных на графике.
    4. `predict_data_line` (dict) — линия прогнозируемых данных:
        - **text** (dict):
            - **en** (str) — описание на английском языке.
            - **ru** (str) — описание на русском языке.
        - **color** (str) — цвет линии прогнозируемых данных.


    Пример вызова API python:
    ------------------
    ```
    import requests
    import pandas as pd

    def func_generate_forecast(df: pd.DataFrame, time_column: str, col_target: str, forecast_horizon_time: str):
        url = "http://your_backend_url/backend/v1/generate_forecast"

        df_records = df.to_dict(orient='records')

        data = {
            "df": df_records,
            "time_column": time_column,
            "col_target": col_target,
            "forecast_horizon_time": forecast_horizon_time
        }

        try:
            response = requests.post(url, json=data)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка при запросе: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None

    df = pd.read_csv(<here yor data>)

    time_column = 'time'
    col_target = 'load_consumption'
    forecast_horizon_time = '2022-09-10 05:00:00'
    df[time_column] = pd.to_datetime(df[time_column])

    response = func_generate_forecast(df, time_column, col_target, forecast_horizon_time)
    ```
    """
    check_permission(user_info=user_info, permission="forecast.quick.create")

    try:
        json_df = body.df
        df = pd.DataFrame(json_df)
        time_column = body.time_column
        col_target = body.col_target
        forecast_horizon_time = body.forecast_horizon_time

        response = await proxy_generate_forecast(df, time_column, col_target, forecast_horizon_time)
        return response

    except Exception as ApplicationError:
        logger.error(ApplicationError.__repr__())
        raise HTTPException(
            status_code=400,
            detail="Unknown Error",
            headers={"X-Error": f"{ApplicationError.__repr__()}"},
        )