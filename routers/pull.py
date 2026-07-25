# FastAPI
from fastapi import APIRouter, Depends

# Application
from dependencies.apikey import apikey_access  # API Key
from dependencies.ip import ip_access  # IP
from schemas.metrics import MetricsSchema

# Collectors
import collectors.system.collector as system
import collectors.load.collector as load
import collectors.memory.collector as memory
import collectors.swap.collector as swap
import collectors.cpu.collector as cpu

# Router
router = APIRouter(
    prefix="",
    tags=["Pull"],
)


@router.get(
    "/pull",
    response_model=MetricsSchema,
    dependencies=[Depends(ip_access), Depends(apikey_access)],
)
async def Pull():
    return MetricsSchema(
        system=system.collect(),
        load=load.collect(),
        memory=memory.collect(),
        swap=swap.collect(),
        cpu=cpu.collect(),
    )
