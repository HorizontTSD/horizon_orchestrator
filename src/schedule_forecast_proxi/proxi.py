import json
from fastapi import HTTPException
import httpx


async def _forward_request(method: str, endpoint: str, params=None, payload=None, headers=None):
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(endpoint, headers=headers, params=params)
            elif method.upper() == "POST":
                response = await client.post(endpoint, json=payload or params, headers=headers)
            elif method.upper() == "DELETE":
                response = await client.request("DELETE", endpoint, data=json.dumps(payload or params) if (payload or params) else None, headers=headers)
            else:
                raise ValueError("Unsupported HTTP method")

            if response.status_code != 200:
                try:
                    error_detail = response.json()
                    detail = error_detail.get("detail", error_detail)
                except (ValueError, json.JSONDecodeError):
                    detail = response.text
                raise HTTPException(status_code=response.status_code, detail=detail)

            try:
                return response.json()
            except (ValueError, json.JSONDecodeError):
                return {"detail": response.text}

        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Forecast service unavailable")
