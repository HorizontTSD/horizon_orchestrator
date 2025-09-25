# src/models.py
from pydantic import BaseModel, EmailStr, RootModel
from typing import Literal, Optional, List, Dict, Any
from datetime import datetime


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


class DataNameListResponse(BaseModel):
    data_names: list[str]




class CreateDBConnectionResponse(BaseModel):
    success: bool
    message: str


class CreateDBConnectionRequest(BaseModel):
    connection_schema: str
    connection_name: str
    db_name: str
    host: str
    port: int
    ssl: bool
    db_user: str
    db_password: str


class DeleteDBConnectionRequest(BaseModel):
    connection_id: int


class DeleteDBConnectionResponse(BaseModel):
    success: bool
    message: str


class DBConnectionResponse(BaseModel):
    id: int
    db_name: str
    connection_name: str | None


class DBConnectionListResponse(BaseModel):
    connections: list[DBConnectionResponse]


class TablesListResponse(BaseModel):
    tables: list[str]


class ColumnsListResponse(BaseModel):
    columns: list[str]


class ForecastConfigRequest(BaseModel):
    connection_id: int
    data_name: str
    source_table: str
    time_column: str
    target_column: str
    count_time_points_predict: int
    target_db: str
    methods: list[str]


class ForecastConfigResponse(BaseModel):
    success: bool
    message: str
    sample_data: list[Any]


class ScheduleForecastingResponse(BaseModel):
    id: int
    organization_id: int
    connection_id: int
    data_name: str


class DeleteForecastResponse(BaseModel):
    success: bool
    message: str


class ScheduleForecastingFullResponse(BaseModel):
    id: int
    organization_id: int
    connection_id: int
    data_name: str
    source_table: str
    time_column: str
    target_column: str
    discreteness: Optional[str]
    count_time_points_predict: Optional[int]
    target_db: Optional[str]
    methods_predict: Optional[List[dict]]
    is_deleted: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class TextTranslation(BaseModel):
    en: str
    ru: str
    zh: str
    it: str
    fr: str
    de: str


class LegendLine(BaseModel):
    text: TextTranslation
    color: str


class Legend(BaseModel):
    last_know_data_line: LegendLine
    real_data_line: LegendLine
    LSTM_data_line: LegendLine
    XGBoost_data_line: LegendLine
    Ensemble_data_line: LegendLine


class MapData(BaseModel):
    data: Any
    last_know_data: Any
    legend: Legend


class MetricTableText(BaseModel):
    en: str
    ru: str
    zh: str
    it: str
    fr: str
    de: str


class MetricTable(BaseModel):
    metrics_table: Any
    text: MetricTableText


class MetrixTables(BaseModel):
    XGBoost: MetricTable
    LSTM: MetricTable


class SensorData(BaseModel):
    description: dict
    map_data: dict
    table_to_download: list
    metrix_tables: dict


class Sensor(RootModel):
    root: Dict[str, "SensorData"]


class GenerateResponse(RootModel):
    root: List[Sensor]


class MethodMetrics(BaseModel):
    MAE: float
    RMSE: float
    R2: float
    MAPE: float

class DateRangeResponse(BaseModel):
    earliest_date: datetime
    max_date: datetime
    start_default_date: datetime
    end_default_date: datetime


class MetricsByMethod(BaseModel):
    MAE: float
    RMSE: float
    R2: float
    MAPE: float


class MetricsResponse(BaseModel):
    metrics: dict[str, MetricsByMethod]


class GenerateDateResponse(RootModel):
    root: Dict[str, DateRangeResponse]


class ForecastMethodsResponse(BaseModel):
    methods: list[str]


class FetchSampleDataRequest(BaseModel):
    connection_id: int
    data_name: str
    source_table: str
    time_column: str
    target_column: str


class FetchSampleResponse(BaseModel):
    sample_data: List[Dict]
    discreteness: int


class TimeIntervalsResponse(BaseModel):
    time_intervals: List[str]