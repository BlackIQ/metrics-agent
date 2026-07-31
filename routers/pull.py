# FastAPI
from fastapi import APIRouter, Depends

# SQLAlchemy
from sqlalchemy.orm import Session

# Datetime
from datetime import datetime, timezone

# Application
from dependencies.apikey import apikey_access  # API Key
from dependencies.ip import ip_access  # IP
from dependencies.database import get_db  # Get Database
from enums.sync import SyncStatus  # Sync enum
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
    db_metrics = (
        db.query(Metric)
        .where(
            Metric.sync_status != SyncStatus.synced,
        )
        .limit(100)
        .all()
    )

    for metric in db_metrics:
        metric.synced_at = datetime.now(timezone.utc)
        metric.sync_status = SyncStatus.synced

    db.commit()

    return db_metrics
