# FastAPI
from fastapi import APIRouter, Depends

# Application
from dependencies.apikey import apikey_access  # API Key
from dependencies.ip import ip_access  # IP

# Router
router = APIRouter(
    prefix="",
    tags=["Pull"],
)


@router.get("/pull", dependencies=[Depends(ip_access), Depends(apikey_access)])
async def Pull():
    return True
