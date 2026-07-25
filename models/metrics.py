# SQLAlchemy
from sqlalchemy import Uuid, JSON, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

# Libs
import uuid
from typing import Any
from enum import StrEnum
from datetime import datetime, timezone

# Application
from base import BaseModel  # Base


# Sync Status Enum
class SyncStatus(StrEnum):
    pending = "pending"
    sending = "sending"
    synced = "synced"
    failed = "failed"


# Metric Model
class Metric(BaseModel):
    __tablename__ = "metrics"

    # Columns
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    collector: Mapped[str] = mapped_column(
        index=True,
        nullable=False,
    )
    sync_status: Mapped[SyncStatus] = mapped_column(
        Enum(SyncStatus),
        default=SyncStatus.pending,
        nullable=False,
    )
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    metrics: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )
