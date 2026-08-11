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


async def save(collector: str, metrics: BaseSchema):
    await asyncio.to_thread(
        _save_sync,
        collector,
        metrics.model_dump(mode="json"),
    )
