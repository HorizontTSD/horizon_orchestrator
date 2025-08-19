# src/api/v1/greeting.py
from fastapi import APIRouter, Body, HTTPException
from src.core.logger import logger
from src.schemas import AlertConfigRequest
from src.services.alert_service import proxy_create_alert
from typing import Annotated
from datetime import date


router = APIRouter()


today = date.today().strftime('%Y-%m-%d')
datetime_today_start = f'{today} 00:00:00'
datetime_today_end = f'{today} 23:59:59'

alert_example = {
    "name": "High CPU Usage Alert",
    "threshold_value": 1000.0,
    "alert_scheme": "Выше значения",
    "trigger_frequency": "Каждый день",
    "message": "Пороговое значение превышено!",
    "telegram_nicknames": ["@user1", "@user2"],
    "email_addresses": ["savvin.nikit@yandex.ru", "user2@example.com"],
    "include_graph": True,
    "date_start": today,
    "date_end": today,
    "time_start": "00:00",
    "time_end": "23:55",
    "start_warning_interval": "60m",
    "sensor_id": "test_id",
    "model": "model_name"

}

@router.post("/create_notification")
async def create_alert(body: Annotated[
    AlertConfigRequest,
    Body(
        example=alert_example
    ),
]):
    """
    Создает YAML-конфигурацию для Alert Manager с параметром предварительного предупреждения.

    **Описание:**
    Данный эндпоинт формирует конфигурацию для системы оповещений, включая параметры срабатывания,
    получателей уведомлений и временные интервалы.

    **Параметры запроса:**
    - **name** (*str*): Название оповещения.
    - **threshold_value** (*float*): Пороговое значение, при достижении которого срабатывает оповещение.
    - **alert_scheme** (*str*): Схема срабатывания ('Выше значения' — при превышении, 'Ниже значения' — при снижении).
    - **trigger_frequency** (*str*): Частота срабатывания (например, 'Каждый день', 'Каждый час').
    - **message** (*str*): Сообщение, отправляемое при срабатывании.
    - **telegram_nicknames** (*List[str]*): Telegram-никнеймы получателей уведомлений.
    - **email_addresses** (*List[str]*): Email-адреса получателей уведомлений.
    - **include_graph** (*bool*): Флаг включения графика в уведомление.
    - **date_start** (*str*): Дата начала действия оповещения ('YYYY-MM-DD').
    - **date_end** (*str*): Дата окончания действия оповещения ('YYYY-MM-DD').
    - **time_start** (*str*): Время начала ('HH:MM').
    - **time_end** (*str*): Время окончания ('HH:MM').
    - **start_warning_interval** (*str*): Интервал предварительного предупреждения ('60m', '1h', и т. д.).
    - **sensor_id** (*str*): Идентификатор сенсора, по которому формируется оповещение.
    - **model** (*str*): Название модели, связанной с оповещением.

    **Ответ:**
    - **200 OK**: YAML-конфигурация успешно создана.
    - **400 Bad Request**: Ошибка валидации входных данных или некорректный формат интервала времени.

    **Исключения:**
    - **HTTPException(400)**: Возникает в случае ошибки при генерации YAML-конфигурации.

    **Пример использования:**
    ```python
    response = requests.post(
        "http://localhost:8000/model_fast_api/v1/create",
        json={
            "name": "High CPU Usage Alert",
            "threshold_value": 100.0,
            "alert_scheme": "Выше значения",
            "trigger_frequency": "Каждый день",
            "message": "Пороговое значение превышено!",
            "telegram_nicknames": ["@user1", "@user2"],
            "email_addresses": ["user@example.com"],
            "include_graph": True,
            "date_start": "2025-02-25",
            "date_end": "2025-02-25",
            "time_start": "00:00",
            "time_end": "23:55",
            "start_warning_interval": "60m",
            "sensor_id": "test_id",
            "model": "model_name"
        }
    )
    print(response.json())
    ```
    """
    try:
        payload = body.dict()
        return await proxy_create_alert(payload)
    except Exception as e:
        logger.error("Error while creating notification: %s", e, exc_info=True)
        raise HTTPException(
                status_code=500,
                detail=f"Внутренняя ошибка: {e}",
                headers={"X-Error": str(e)},
            )