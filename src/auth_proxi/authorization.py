from environs import Env
from fastapi import APIRouter, Body, HTTPException
from src.schemas import AuthResponse, AuthRequest, LogoutResponse, LogoutRequest, RefreshRequest, RefreshResponse
import httpx

env = Env()
env.read_env()

auth_service_url = env.str("AUTH_SERVICE", "LOCAL")

router = APIRouter()

@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Авторизация пользователей",
    description="Прокси-эндпоинт для авторизации и получения refresh и access токенов"
)
async def proxy_auth_user(auth_data: AuthRequest = Body(..., example={"login": "test_user", "password": "qwerty123"})):
    """
    Эндпоинт для авторизации пользователей приложения

    Description:
    - Предназначен для фронтэнда для авторизации и получения refresh и access токенов

    Returns:
    - **JSON**:
        - `access_token`: токен, предназначенный для авторизованного доступа
        - `refresh_token`: токен для обновления access_token
        - `token_type`: тип токена
        - `expires_in`: длительность access_token
        - `refresh_expires_in`: длительность refresh_token
        - `user`: {
                `id`: id пользователя
                `organization_id`: id организации пользователя
                `roles`: роли пользователя
                `permissions`: права пользователя
            }

    Example Response:
    ```json
        {
            "access_token": "jwt",
            "refresh_token": "jwt",
            "token_type": "Bearer",
            "expires_in": 900,
            "refresh_expires_in": 2592000,
            "user": {
                "id": 123,
                "organization_id": 1,
                "roles": ["admin", ...],
                "permissions": [...]
            }
        }
    ```

    Raises:
    - **HTTPException 400**: При ошибке валидации входных данных
    - **HTTPException 401**: При неверных учётных данных
    - **HTTPException 401**: Если пользователь заблокирован, удалён или неактивен
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{auth_service_url}/api/v1/auth/login", json=auth_data.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()



@router.post(
    "/logout",
    response_model=LogoutResponse,
    summary="Выход пользователя",
    description="Прокси-эндпоинт для инвалидации refresh-токена пользователя"
)
async def proxy_logout_user(logout_data: LogoutRequest = Body(..., example={"refresh_token": "eyCshr3bGciOihfd4S1NsaIsInR5da25CLKpikpXVCJ9.eyJzdWIiOi....."})):
    """
    Эндпоинт для инвалидации refresh-токена пользователя

    Description:
    - Предназначен для фронтэнда для инвалидации refresh-токена пользователя

    Returns:
    - **JSON**:
        - `detail`: детали ответа

    Example Response:
    ```json
        {
            "detail": "Logout successful"
        }
    ```

    Raises:
    - **HTTPException 401**: При невалидном токене
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{auth_service_url}/api/v1/auth/logout", json=logout_data.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()



@router.post(
    "/refresh",
    response_model=RefreshResponse,
    summary="Refresh access-token",
    description="""
    Обновляет access-token по refresh-token с ротацией:
    - Проверяет подпись и срок действия refresh-токена
    - Проверяет, что refresh-токен не отозван и существует
    - Помечает старый refresh как revoked
    - Генерирует новый refresh и access
    - Возвращает пару токенов
    """
)
async def proxy_refresh_tokens(
        request: RefreshRequest = Body(
            ...,
            example={
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
            }
        )
):
    """
    Эндпоинт для обновления JWT токенов по refresh-токену.

    Description:
    - Реализует безопасную ротацию токенов с защитой от повторного использования
    - Проверяет валидность и срок действия refresh-токена
    - Отзывает использованный токен и выдает новую пару токенов
    - Возвращает обновленные access и refresh токены

    Raises:
    - **HTTPException 401**: Если refresh-токен недействителен, истек или отозван
    - **HTTPException 500**: Если произошла ошибка при работе с базой данных или в сервисе
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{auth_service_url}/api/v1/auth/refresh", json=request.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()