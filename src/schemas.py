# src/models.py

from pydantic import BaseModel
from typing import List, Dict


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

