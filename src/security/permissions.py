from fastapi import HTTPException, status


def check_permission(user_info: dict, permission: str):
    if permission not in user_info.get('permissions', []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав для выполнения этой операции"
        )