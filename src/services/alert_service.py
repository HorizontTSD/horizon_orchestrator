import json
import httpx
from fastapi import HTTPException, Request
from environs import Env
from src.core.logger import logger

env = Env()
env.read_env()

BASE_URL = env.str('ALERT_SERVICE')


async def proxy_create_alert(payload: dict) -> dict:
    url = f"{BASE_URL}/alert_manager/v1/create"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()  # убираем await
    except httpx.HTTPStatusError as e:
        try:
            detail = e.response.json().get("detail", e.response.text)  # убираем await
        except Exception:
            detail = e.response.text
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def proxy_notification_delete(body: dict) -> dict:
    url = f"{BASE_URL}/alert_manager/v1/delete"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.request(
                "DELETE", url, content=json.dumps(body), headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        try:
            detail = e.response.json().get("detail", e.response.text)
        except Exception:
            detail = e.response.text
        logger.error("HTTPStatusError while deleting notification: %s", detail, exc_info=True)
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except httpx.RequestError as e:
        logger.error("RequestError while deleting notification: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        logger.error("Unexpected error while deleting notification: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def notification_list() -> dict:
    url = f"{BASE_URL}/alert_manager/v1/list"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        try:
            detail = e.response.json().get("detail", e.response.text)
        except Exception:
            detail = e.response.text
        logger.error("HTTPStatusError while fetching notification list: %s", detail, exc_info=True)
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except httpx.RequestError as e:
        logger.error("RequestError while fetching notification list: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        logger.error("Unexpected error while fetching notification list: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
