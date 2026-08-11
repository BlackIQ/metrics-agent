# Asyncio
import asyncio

# Datetime
from datetime import datetime, timedelta, timezone

# Application
from core.logger import get_logger  # Logger
from database.database import session  # Database
from models import Metric  # Models
from enums.sync import SyncStatus  # Enums

# Logger (Cleanup)
logger = get_logger("cleanup")


async def cleanup_old_metrics(retention_days: int = 7):
    while True:
        try:
            cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

            db = session()

            db_metrics = (
                db.query(Metric)
                .where(
                    Metric.sync_status == SyncStatus.synced,
                    Metric.synced_at <= cutoff,
                )
                .all()
            )

            for metric in db_metrics:
                db.delete(metric)

            db.commit()

            if len(db_metrics) > 0:
                logger.info(
                    f"Cleaned up {count} synced metrics older than {retention_days} days."
                )
        except Exception as e:
            logger.error(f"Error during metric cleanup: {e}", exc_info=True)

        await asyncio.sleep(21600)
