# src/api/v1/proxy_schedule_forecast/dbconnection_endpoints.py
from fastapi import APIRouter, Depends, Body, Path, Query, HTTPException, status
from src.core.token import token_validator 
from src.services.proxy_schedule_forecast_service import (
    proxy_create_dbconnection,
    proxy_delete_dbconnection,
    proxy_list_dbconnections,
    proxy_get_connection_tables,
    proxy_get_connection_table_columns
)
from src.model import ProxyError 

router = APIRouter(prefix="/db_connection", tags=["Proxy Schedule Forecast DB Connection"])

@router.post("/create", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_create_dbconnection_endpoint(
    payload: dict = Body(...), 
    token: str = Depends(token_validator)
):
    response = await proxy_create_dbconnection(token, payload)
    return await handle_proxy_response(response)

@router.delete("/delete/{connection_id}", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_delete_dbconnection_endpoint(
    connection_id: int = Path(...),
    token: str = Depends(token_validator)
):
    response = await proxy_delete_dbconnection(token, connection_id)
    return await handle_proxy_response(response)

@router.get("/list", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_list_dbconnections_endpoint(token: str = Depends(token_validator)):
    response = await proxy_list_dbconnections(token)
    return await handle_proxy_response(response)

@router.get("/{connection_id}/tables", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_get_connection_tables_endpoint(
    connection_id: int = Path(...),
    token: str = Depends(token_validator)
):
    response = await proxy_get_connection_tables(token, connection_id)
    return await handle_proxy_response(response)

@router.get("/{connection_id}/{table_name}/columns", responses={503: {"model": ProxyError}, 500: {"model": ProxyError}})
async def proxy_get_connection_table_columns_endpoint(
    connection_id: int = Path(...),
    table_name: str = Path(...),
    token: str = Depends(token_validator)
):
    response = await proxy_get_connection_table_columns(token, connection_id, table_name)
    return await handle_proxy_response(response)

async def handle_proxy_response(response: httpx.Response):
    try:
        try:
            data = response.json()
        except:
            data = response.text

        if 200 <= response.status_code < 300:
             return data
        else:
            raise HTTPException(status_code=response.status_code, detail=data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
