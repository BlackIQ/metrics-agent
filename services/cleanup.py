# Asyncio
import asyncio

# Datetime
from datetime import datetime, timedelta, timezone

# Application
from database.database import session  # Database
from models import Metric  # Models
from enums.sync import SyncStatus  # Enums


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
                print(f"Cleaned up {len(db_metrics)} synced metrics.")
        except Exception as e:
            print(f"Error during metric cleanup: {e}")

        await asyncio.sleep(21600)
