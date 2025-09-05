from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from environs import Env

env = Env()
env.read_env()
auth_service_url = env.str("AUTH_SERVICE", "LOCAL")

auth_scheme = HTTPBearer()

async def access_token_validator(credentials: HTTPAuthorizationCredentials = Security(auth_scheme)):
    token = credentials.credentials
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{auth_service_url}/api/v1/check/access_token",
                headers={"authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid access token")
        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Auth service unavailable")
    return response.json()
