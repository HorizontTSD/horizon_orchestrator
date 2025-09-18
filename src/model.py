# src/model.py

from pydantic import BaseModel


class HellowRequest(BaseModel):
    names: list[str]

class ProxyError(BaseModel):
    detail: str
    message: str