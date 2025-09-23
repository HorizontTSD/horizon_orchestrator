import httpx
from fastapi import HTTPException, Request
from environs import Env
from src.core.logger import logger
import pandas as pd

env = Env()
env.read_env()

BASE_URL = env.str('BACKEND_SERVICE')
BACKEND_TOKEN = env.str("BACKEND_TOKEN")


async def proxi_generate_possible_date(df: pd.DataFrame, time_column: str) -> dict:
    url = f"{BASE_URL}/api/v1/possible-date/"
    df_records = df.to_dict(orient='records')

    payload = {
        "df": df_records,
        "time_column": time_column
    }
    headers = {
        "Authorization": f"Bearer {BACKEND_TOKEN}"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        try:
            detail = e.response.json().get("detail", e.response.text)
        except Exception:
            detail = e.response.text
        logger.error(f"HTTPStatusError in func [proxi_generate_possible_date] {e.response.status_code}: {detail}")
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except httpx.RequestError as e:
        logger.error(f"RequestError: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        logger.exception("Unexpected error in proxi_generate_possible_date")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def proxy_generate_forecast(
        df: pd.DataFrame,
        time_column: str,
        col_target: str,
        forecast_horizon_time: str
) -> dict:

    url = f"{BASE_URL}/api/v1/predict-xgboost"

    df_records = df.to_dict(orient='records')

    payload = {
        "df": df_records,
        "time_column": time_column,
        "col_target": col_target,
        "forecast_horizon_time": forecast_horizon_time
    }

    headers = {
        "Authorization": f"Bearer {BACKEND_TOKEN}"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        try:
            detail = e.response.json().get("detail", e.response.text)
        except Exception:
            detail = e.response.text
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
