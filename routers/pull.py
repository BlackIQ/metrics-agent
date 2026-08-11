# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import select

# Datetime
from datetime import datetime, timezone

# Application
from core.logger import get_logger  # Logger
from dependencies.apikey import apikey_access
from dependencies.ip import ip_access
from dependencies.database import get_db
from enums.sync import SyncStatus
from schemas.metrics import ReadMetricsSchema, AckSchema
from models import Metric

# Logger (Pull)
logger = get_logger("router.pull")

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
async def pull_metrics(
    limit: int = 100,
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)

    db_metrics = (
        db.query(Metric)
        .where(Metric.sync_status != SyncStatus.synced)
        .order_by(Metric.collected_at.asc())
        .limit(limit)
        .all()
    )

    if not db_metrics:
        return []

    for metric in db_metrics:
        metric.sync_status = SyncStatus.processing
        metric.attempts += 1
        metric.last_attempt_at = now

    db.commit()

    logger.info(f"Dispatched {len(db_metrics)} metrics to cloud pull client.")

    return db_metrics


@router.post(
    "/ack",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(ip_access), Depends(apikey_access)],
)
async def acknowledge_metrics(
    payload: AckSchema,
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)

    stmt = select(Metric).where(Metric.id.in_(payload.metric_ids))
    db_metrics = db.scalars(stmt).all()

    if not db_metrics:
        logger.warning(
            f"ACK failed: No metrics found matching IDs {payload.metric_ids}"
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No matching metric records found for given IDs",
        )

    for metric in db_metrics:
        metric.sync_status = SyncStatus.synced
        metric.synced_at = now

    db.commit()

    logger.info(f"Acknowledged {len(db_metrics)} metrics.")

    return {"message": f"Successfully acknowledged {len(db_metrics)} metrics"}
