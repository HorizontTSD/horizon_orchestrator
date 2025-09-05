from environs import Env
from fastapi import APIRouter, Body, HTTPException, status, Request, Depends
from src.schemas import (
    RegisterUserRequest, RegisterUserResponse,
    RolesResponse, PermissionsResponse, GetUsersByOrgResponse
)
from src.security.check_token import access_token_validator

import httpx

env = Env()
env.read_env()

auth_service_url = env.str("AUTH_SERVICE", "LOCAL")

router = APIRouter()

@router.post(
    "/user",
    response_model=RegisterUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user in organization",
    description="""
    Эндпоинт для регистрации нового пользователя в организации.

    Description:
    - Создаёт нового пользователя, связанного с организацией из токена авторизации.
    - Назначает пользователю указанную роль.
    - Требует действующий JWT access_token с ролью 'superuser'.
    """
)
async def proxy_register_user(
        request: Request,
        payload: RegisterUserRequest = Body(
            ...,
            example={
                "login": "new_user",
                "password": "secure_password123",
                "email": "newuser@example.com",
                "first_name": "Иван",
                "last_name": "Петров",
                "role": "user"
            }
        ),
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для регистрации нового пользователя в организации.

    Description:
    - Создаёт нового пользователя, связанного с организацией из токена авторизации.
    - Назначает пользователю указанную роль.
    - Требует действующий JWT access_token с ролью 'superuser'.

    Raises:
    - **HTTPException 400**: Если указанная роль не существует.
    - **HTTPException 401**: Если access_token отсутствует, истёк или недействителен.
    - **HTTPException 403**: Если у пользователя нет роли 'superuser'.
    - **HTTPException 409**: Если логин или email нового пользователя уже существуют.
    - **HTTPException 500**: Если произошла ошибка при работе с базой данных.
    """
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{auth_service_url}/api/v1/register/user",
            json=payload.dict(),
            headers=headers
        )
        if response.status_code != status.HTTP_201_CREATED:
            try:
                error_detail = response.json()
            except ValueError:
                error_detail = {"detail": response.text}
            raise HTTPException(status_code=response.status_code, detail=error_detail.get("detail", error_detail))
        return response.json()


@router.get(
    "/roles_list",
    response_model=RolesResponse,
    summary="Список ролей",
    description="Прокси-эндпоинт для получения списка ролей")
async def proxy_get_roles(_=Depends(access_token_validator)):
    """
    Эндпоинт для получения данных для выпадающего списка ролей.

    Description:
    - Предназначен для фронтэнда для получения значений для выпадающего списка.
    - Возвращает `roles` — плоский список всех ролей, чтобы заполнить выпадающий список.

    Raises:
    - **HTTPException 500**: При ошибке выполнения SQL запросов
    - **HTTPException 503**: При ошибке подключения к базе данных
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_service_url}/api/v1/register_metadata/roles_list")
        if response.status_code != 200:
            try:
                error_detail = response.json()
            except ValueError:
                error_detail = {"detail": response.text}
            raise HTTPException(status_code=response.status_code, detail=error_detail.get("detail", error_detail))
        return response.json()



@router.get(
    "/permissions_list",
    response_model=PermissionsResponse,
    summary="Список разрешений",
    description="Прокси-эндпоинт для получения списка разрешений")
async def proxy_get_permissions(_=Depends(access_token_validator)):
    """
    Эндпоинт для получения данных для выпадающего списка разрешений.

    Description:
    - Предназначен для фронтэнда для получения значений для выпадающего списка.
    - Возвращает `permissions` — плоский список всех кодов разрешений, чтобы заполнить выпадающий список.

    Raises:
    - **HTTPException 500**: Если произошла ошибка при подключении к базе или получении разрешений.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_service_url}/api/v1/register_metadata/permissions_list")
        if response.status_code != 200:
            try:
                error_detail = response.json()
            except ValueError:
                error_detail = {"detail": response.text}
            raise HTTPException(status_code=response.status_code, detail=error_detail.get("detail", error_detail))
        return response.json()



@router.get(
    "/{organization_id}/users",
    response_model=GetUsersByOrgResponse,
    summary="Get organization's users",
    description="Прокси-эндпоинт для получения списка пользователей организации с их ролями и разрешениями"
)
async def proxy_get_users_by_org(
        organization_id: int,
        request: Request,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для получения списка пользователей организации.

    Description:
    - Возвращает список активных пользователей указанной организации
    - Для каждого пользователя показывает его роли и разрешения
    - Поддерживает иерархию ролей через таблицу user_roles
    - Фильтрует удаленных и неактивных пользователей

    Parameters:
    - **organization_id** (integer, path): ID организации для получения списка пользователей

    Raises:
    - **HTTPException 401**: Если пользователь не авторизован (нет валидного токена)
    - **HTTPException 500**: Если произошла ошибка при работе с auth-сервисом
    """
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{auth_service_url}/api/v1/organizations/{organization_id}/users",
                headers=headers
            )
            if response.status_code != 200:
                try:
                    error_detail = response.json()
                except ValueError:
                    error_detail = {"detail": response.text}
                raise HTTPException(status_code=response.status_code, detail=error_detail.get("detail", error_detail))
            return response.json()
        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Auth service unavailable")