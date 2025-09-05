# src/api/v1/greeting.py
from fastapi import APIRouter, HTTPException, Depends
from src.core.logger import logger
from src.services.mini_charts_data_fetcher_service import mini_charts_data
from src.security.check_token import access_token_validator
from src.security.permissions import check_permission
from src.security.permissions import check_permission


router = APIRouter()


@router.get("/get_mini_charts_data")
async def func_get_mini_charts_data(user_info = Depends(access_token_validator)):
    """
    Возвращает данные для дополнительных мини-графиков.

    Формат возвращаемых данных:
    {[
        mini_graph_data,
        mini_graph_data,
        ...
    ]}

    Где `id` (str) обозначает позицию отображения мини-графика, а `mini_graph_data` содержит следующие ключи:

    1. **title** (dict) — заголовок мини-графика:
        - "en" (str) — название на английском.
        - "ru" (str) — название на русском.

    2. **values** (str) — текущее значение параметра с единицей измерения.

    3. **description** (dict) — краткое описание мини-графика:
        - "en" (str) — описание на английском.
        - "ru" (str) — описание на русском.

    4. **percentages** (dict) — изменение показателя в процентах:
        - "value" (float) — числовое значение изменения.
        - "mark" (str) — направление изменения ("positive" или "negative").

    5. **data** (list/dict) — данные для построения мини-графика.
    """

    check_permission(user_info=user_info, permission="dashboard.view")

    try:
        response = await mini_charts_data()
        return response

    except Exception as ApplicationError:
        logger.error(ApplicationError.__repr__())
        raise HTTPException(
            status_code=400,
            detail="Unknown Error",
            headers={"X-Error": f"{ApplicationError.__repr__()}"},
        )
