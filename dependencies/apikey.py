# FastAPI
from fastapi import status, Security, HTTPException
from fastapi.security import APIKeyHeader

# Application
from core.settings import settings  # Settings

# Header Schema for API Key
header_schema = APIKeyHeader(
    name="X-API-KEY",
    description="API Key defined in dashbboard",
)


# API Key Dependency
async def apikey_access(api_key: str = Security(header_schema)) -> bool:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return True
