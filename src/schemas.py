# src/models.py
from pydantic import BaseModel, EmailStr
from typing import Literal, Optional, List, Dict


class HellowRequest(BaseModel):
    names: list[str]


class ForecastData(BaseModel):
    sensor_ids: List[str]


class AlertConfigRequest(BaseModel):
    name: str
    threshold_value: float
    alert_scheme: str
    trigger_frequency: str
    message: str
    telegram_nicknames: List[str]
    email_addresses: List[str]
    include_graph: bool
    date_start: str
    date_end: str
    time_start: str
    time_end: str
    start_warning_interval: str
    sensor_id: str
    model: str


class DeleteAlertRequest(BaseModel):
    filename: str


class PredictRequest(BaseModel):
    df: List[Dict]
    time_column: str
    col_target: str
    forecast_horizon_time: str



class ConvertRequest(BaseModel):
    df: List[Dict]
    time_column: str


class MetrixByPeriod(BaseModel):
    sensor_ids: List[str]
    date_start: str
    date_end: str


class PossibleData(ForecastData):
    pass


# Auth shemas



class PermissionsResponse(BaseModel):
    permissions: List[str]


class RegistrationRequest(BaseModel):
    organization_name: str
    organization_email: EmailStr
    superuser_login: str
    superuser_first_name: str
    superuser_last_name: str
    superuser_email: EmailStr
    superuser_password: str
    verify_superuser_email: Optional[bool] = False
    verify_organization_email: Optional[bool] = False


class RegistrationResponse(BaseModel):
    organization_id: int
    superuser_id: int
    access_token: str
    refresh_token: str
    message: str = "Организация и суперюзер успешно зарегистрированы"


class UserResponse(BaseModel):
    login: str
    first_name: str
    last_name: str
    email: str
    access_level: str  # например, 'admin'
    permissions: List[str]


class GetUsersByOrgResponse(BaseModel):
    users: List[UserResponse]


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["Bearer"]
    expires_in: int
    refresh_expires_in: int

class AuthRequest(BaseModel):
    login: str | EmailStr
    password: str


class UserAuthResponse(BaseModel):
    id: int
    organization_id: int
    roles: list[str]
    permissions: list[str]


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    refresh_expires_in: int
    user: UserAuthResponse


class RolesResponse(BaseModel):
    roles: list[str]


class RegisterUserRequest(BaseModel):
    """
    Схема для запроса на регистрацию нового пользователя в организации.
    """
    login: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str

class RegisterUserResponse(BaseModel):
    """
    Схема для ответа на запрос регистрации нового пользователя.
    """
    success: bool
    user_id: int
    message: str


class LogoutRequest(BaseModel):
    refresh_token: str


class LogoutResponse(BaseModel):
    detail: str


class UserStatusChangeResponse(BaseModel):
    """
    Схема для ответа на запрос по изменению статуса пользователя из организации.
    """
    success: bool
    user_id: int
    message: str


class UserStatusChangeRequest(BaseModel):
    """
    Схема для ответа по изменению статуса пользователя из организации.
    """
    login_to_change: str

