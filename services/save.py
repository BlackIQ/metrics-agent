# Async
import asyncio

# Datetime
from datetime import datetime, timezone

# Application
from core.logger import get_logger  # Logger
from database.database import session  # Database
from models import Metric  # Models
from base import BaseSchema  # Base

# Logger (Save)
logger = get_logger("save")


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

        logger.debug(f"Metric '{collector}' saved to SQLite buffer.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save metric '{collector}': {e}", exc_info=True)
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
