# src/api/v1/greeting.py
from fastapi import APIRouter, Body, HTTPException, Depends
from src.services.alert_service import proxy_notification_delete
from src.security.check_token import access_token_validator
from src.security.permissions import check_permission


router = APIRouter()


@router.delete("/notification_delete")
async def delete_alert(
        body: dict = Body(
            example={"filename": "alert_config_123456.yaml"}
        ),
        user_info=Depends(access_token_validator)
):
    """
    Асинхронная функция для удаления YAML-конфигурации оповещения.

    **Описание:**
    Функция удаляет YAML-файл конфигурации, если он существует, и возвращает соответствующее сообщение.
    Если файл не найден, функция уведомляет об этом.

    **Параметры:**
    - **filename** (*str*): Название YAML-файла, который необходимо удалить.

    **Возвращает:**
    - **str**: Сообщение о результате удаления:
      - `"Файл {filename} успешно удален."`, если файл был найден и удален.
      - `"Файл {filename} не найден."`, если файл отсутствует.

    **Исключения:**
    - **HTTPException (400)**: Если переданный `filename` не имеет расширения `.yaml`.

    **Пример использования:**
    ```python
    response = await delete_alert_config("alert_config.yaml")
    print(response)  # "Файл alert_config.yaml успешно удален."
    ```
    """
    check_permission(user_info=user_info, permission="notification.delete")

    try:
        result = await proxy_notification_delete(body)
        return result
    except HTTPException as e:
        raise e