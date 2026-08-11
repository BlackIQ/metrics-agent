# Async
import asyncio

# Datetime
from datetime import datetime, timezone

# Application
from database.database import session  # Database
from models import Metric  # Models
from base import BaseSchema  # Base


def _save_sync(collector: str, metrics_data: dict):
    db = session()

    try:
        db_metric = Metric(
            collector=collector,
            metrics=metrics_data,
            collected_at=datetime.now(timezone.utc),
        )
        db.add(db_metric)
        db.commit()

        print(f"Metric of {collector} is saved")
    finally:
        db.close()


async def save(collector: str, metrics: BaseSchema | dict):
    if isinstance(metrics, BaseSchema):
        data = metrics.model_dump(mode="json")
    elif isinstance(metrics, dict):
        data = metrics
    else:
        data = dict(metrics)

    await asyncio.to_thread(_save_sync, collector, data)
