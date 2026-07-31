# FastAPI
from fastapi import APIRouter, Depends

# Application
from dependencies.apikey import apikey_access  # API Key
from dependencies.ip import ip_access  # IP
from schemas.message import MessageSchema  # Schemas

# Router
router = APIRouter(
    prefix="",
    tags=["Health Check"],
)


@router.get(
    "/ping",
    response_model=MessageSchema,
    dependencies=[Depends(ip_access), Depends(apikey_access)],
)
async def ping():
    return MessageSchema(
        message="Pong",
    )
