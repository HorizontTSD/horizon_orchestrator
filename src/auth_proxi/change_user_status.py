from fastapi import APIRouter, HTTPException, Depends, Body, status, Request
from src.schemas import UserStatusChangeResponse, UserStatusChangeRequest
from src.auth_proxi.check_token import access_token_validator
from environs import Env
import httpx

env = Env()
env.read_env()
auth_service_url = env.str("AUTH_SERVICE", "LOCAL")

router = APIRouter()


@router.post("/block", response_model=UserStatusChangeResponse, status_code=status.HTTP_200_OK)
async def proxy_block_user(
        payload: UserStatusChangeRequest = Body(
            ...,
            example={"login_to_change": "test_user_for_del"}
        ),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для блокирования пользователя в организации.

    Description:
    - Помечает пользователя с указанным логином как заблокированного (is_block=True, is_active=False).
    - Блокировка выполняется через auth-сервис.
    - Требуется действующий access_token.

    Raises:
    - **HTTPException 401**: Если access_token отсутствует или недействителен.
    - **HTTPException 500**: Если произошла ошибка при работе с auth-сервисом.
    """
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{auth_service_url}/api/v1/change_user_status/block",
                json=payload.dict(),
                headers=headers
            )
            if response.status_code != 200:
                try:
                    error_detail = response.json()
                except ValueError:
                    error_detail = {"detail": response.text}
                raise HTTPException(status_code=response.status_code,
                                    detail=error_detail.get("detail", error_detail))
            return response.json()
        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Auth service unavailable")


@router.post("/unblock", response_model=UserStatusChangeResponse, status_code=status.HTTP_200_OK)
async def proxy_unblock_user(
        payload: UserStatusChangeRequest = Body(
            ...,
            example={"login_to_change": "test_user_for_del"}
        ),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для разблокирования пользователя в организации.

    Description:
    - Помечает пользователя с указанным логином как разблокированного (is_block=False, is_active=True).
    - Разблокировка выполняется через auth-сервис.
    - Требуется действующий access_token.

    Raises:
    - **HTTPException 401**: Если access_token отсутствует или недействителен.
    - **HTTPException 500**: Если произошла ошибка при работе с auth-сервисом.
    """
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{auth_service_url}/api/v1/change_user_status/unblock",
                json=payload.dict(),
                headers=headers
            )
            if response.status_code != 200:
                try:
                    error_detail = response.json()
                except ValueError:
                    error_detail = {"detail": response.text}
                raise HTTPException(status_code=response.status_code,
                                    detail=error_detail.get("detail", error_detail))
            return response.json()
        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Auth service unavailable")


@router.delete("/delete", response_model=UserStatusChangeResponse, status_code=status.HTTP_200_OK)
async def proxy_delete_user(
        payload: UserStatusChangeRequest = Body(
            ...,
            example={"login_to_change": "test_user_for_del"}
        ),
        request: Request = None,
        _=Depends(access_token_validator)
):
    """
    Эндпоинт для удаления пользователя из организации.

    Description:
    - Помечает пользователя с указанным логином как удалённого (is_deleted=True).
    - Удаление выполняется через auth-сервис.
    - Требуется действующий access_token.

    Raises:
    - **HTTPException 401**: Если access_token отсутствует или недействителен.
    - **HTTPException 500**: Если произошла ошибка при работе с auth-сервисом.
    """
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                f"{auth_service_url}/api/v1/change_user_status/delete",
                json=payload.dict(),
                headers=headers
            )
            if response.status_code != 200:
                try:
                    error_detail = response.json()
                except ValueError:
                    error_detail = {"detail": response.text}
                raise HTTPException(status_code=response.status_code,
                                    detail=error_detail.get("detail", error_detail))
            return response.json()
        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Auth service unavailable")
