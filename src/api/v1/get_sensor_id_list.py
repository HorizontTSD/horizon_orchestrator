# src/api/v1/greeting.py
from fastapi import APIRouter, HTTPException, Depends
from src.core.logger import logger
from src.services.sensor_list_fetcher_service import get_sensor_list_by_org
from src.security.check_token import access_token_validator
from src.security.permissions import check_permission


router = APIRouter()

@router.get("/get_sensor_id_list")
async def func_get_sensor_id_list(user_info=Depends(access_token_validator)):
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
    check_permission(user_info=user_info, permission="dashboard.view")

    org_id = user_info.get("org_id", None)

    try:
        response = await get_sensor_list_by_org(org_id)
        return response

    except Exception as ApplicationError:
        logger.error(ApplicationError.__repr__())
        raise HTTPException(
            status_code=400,
            detail="Unknown Error",
            headers={"X-Error": f"{ApplicationError.__repr__()}"},
        )