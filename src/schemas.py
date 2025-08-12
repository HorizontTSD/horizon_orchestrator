# src/models.py

from pydantic import BaseModel
from typing import List, Dict


class HellowRequest(BaseModel):
    names: list[str]


class ForecastData(BaseModel):
    sensor_ids: List[str]