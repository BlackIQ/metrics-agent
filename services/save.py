# Datetime
from datetime import datetime, timezone

# Application
from base import BaseSchema  # Base schema
from models import Metric  # Metric model
from database.database import session


async def save(collector: str, metrics: BaseSchema):
    db = session()

    try:
        db_metric = Metric(
            collector=collector,
            metrics=metrics.model_dump(mode="json"),
            collected_at=datetime.now(timezone.utc),
        )

        db.add(db_metric)

        db.commit()

        db.refresh(db_metric)

        print(f"Metrics of {collector} saved.")
    finally:
        db.close()
