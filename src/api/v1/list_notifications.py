# src/api/v1/greeting.py
from fastapi import APIRouter, Body, HTTPException
from src.services.alert_service import notification_list


router = APIRouter()


@router.get("/notification_list")
async def notifications_list():
    """
    Асинхронная функция для получения списка YAML-файлов и их содержимого.

    **Описание:**
    Функция просматривает указанную директорию, находит все файлы с расширением `.yaml`,
    считывает их содержимое и возвращает в формате JSON.

    **Возвращает:**
    - **List[Dict[str, Dict]]**: Список словарей, где каждый словарь содержит данные из файла
      и его название в поле `"file_name"`.

    **Исключения:**
    - **HTTPException (404)**: Если указанная директория с YAML-файлами не найдена.
    - **HTTPException (500)**: Если возникает ошибка при чтении какого-либо YAML-файла.

    **Пример использования:**
    ```python
    yaml_files = await list_yaml_files_with_content()
    for file in yaml_files:
        print(file["file_name"], file)  # Выведет название файла и его содержимое
    ```

    **Дополнительно:**
    - Данные из каждого YAML-файла загружаются с помощью `yaml.safe_load()`.
    - В результат добавляется поле `"file_name"`, содержащее имя файла.
    """
    try:
        result = await notification_list()
        return result
    except HTTPException as e:
        raise e
