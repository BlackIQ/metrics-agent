# FastAPI
from fastapi import APIRouter, Depends

# SQLAlchemy
from sqlalchemy.orm import Session

# Application
from dependencies.apikey import apikey_access  # API Key
from dependencies.ip import ip_access  # IP
from dependencies.database import get_db  # Get Database
from schemas.metrics import ReadMetricsSchema  # Schemas
from models import Metric  # Models

# Router
router = APIRouter(
    prefix="",
    tags=["Pull"],
)


@router.get(
    "/pull",
    response_model=list[ReadMetricsSchema],
    dependencies=[Depends(ip_access), Depends(apikey_access)],
)
async def Pull(db: Session = Depends(get_db)):
    db_metrics = db.query(Metric).limit(10).all()

    return db_metrics
