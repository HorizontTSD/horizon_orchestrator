import os
import pandas as pd
from fastapi import APIRouter, Body, HTTPException, Depends
from src.core.logger import logger
from typing import Annotated
from src.schemas import ConvertRequest
from src.services.tool_backend_service import proxi_generate_possible_date
from src.auth_proxi.check_token import access_token_validator

home_path = os.getcwd()


router = APIRouter()

example_df = pd.read_csv(f'{home_path}/src/examples/example_data.csv')
example_df_short = example_df.iloc[:1000]

example_df_json_short= example_df_short.to_dict(orient="records")


@router.post("/generate_possible_date")
async def func_generate_possible_date(body: Annotated[
    ConvertRequest, Body(
        example={
            "df": example_df_json_short,
            "time_column": "time"
        })],
        _=Depends(access_token_validator)
):

    """
    Генерирует возможный диапазон дат и времени для пользовательского прогноза для фронта на основе временного столбца DataFrame.

    Описание:
    ----------
    Функция вычисляет интервал времени между записями и прогнозирует возможный диапазон дат.
    Минимальная дата (`min`) — это `last_know_date`, взятая из первой записи столбца `time_column`.
    Максимальная дата (`max`) определяется как `5%` от длины DataFrame в будущем, с учётом вычисленного интервала времени.
    Также возвращается параметр `min_forecast_horizon_time`, который обозначает минимально возможную дату для выбора пользователем.

    Параметры:
    ----------
    df : pd.DataFrame
        DataFrame, содержащий временные данные.
    time_column : str
        Название столбца, содержащего временные метки.

    Возвращает:
    ----------
    dict:
        - `date`: словарь с минимальной (`min`) и максимальной (`max`) датами.
        - `min_forecast_horizon_time`: минимально возможная дата для выбора пользователем.
        - `time_hour`: список возможных значений часов (от `0` до `23`).
        - `time_minute`: список возможных значений минут (от `0` до `59`).

    Формат возвращаемого JSON:
    --------------------------
    ```json
    {
        "date": {
            "min": "2024-01-01",
            "max": "2024-02-15"
        },
        "min_forecast_horizon_time": "2024-01-01",
        "time_hour": [0, 1, 2, ..., 23],
        "time_minute": [0, 1, 2, ..., 59]
    }
    ```

    Пример использования:
    ---------------------
    ```python
    import requests

    def func_generate_possible_date(df: pd.DataFrame, time_column: str):
        url = url_backend + '/generate_possible_date'
        df_records = df.to_dict(orient='records')

        data = {
            "df": df_records,
            "time_column": time_column
        }

        try:
            response = requests.post(url, json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None

    response = func_generate_possible_date(df, time_column)
    print(response)
    ```
    """
    try:
        json_df = body.df
        df = pd.DataFrame(json_df)
        time_column = body.time_column
        response = await proxi_generate_possible_date(df=df, time_column=time_column)
        return response

    except Exception as ApplicationError:
        logger.error(ApplicationError.__repr__())
        raise HTTPException(
            status_code=400,
            detail="Unknown Error",
            headers={"X-Error": f"{ApplicationError.__repr__()}"},
        )
