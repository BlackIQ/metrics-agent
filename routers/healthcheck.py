# FastAPI
from fastapi import APIRouter, Depends

# Application
from dependencies.apikey import apikey_access  # API Key
from dependencies.ip import ip_access  # IP

# Router
router = APIRouter(
    prefix="",
    tags=["Health Check"],
)


@router.get("/ping", dependencies=[Depends(ip_access), Depends(apikey_access)])
async def ping():
    return {"message": "Route: /api/ping"}
