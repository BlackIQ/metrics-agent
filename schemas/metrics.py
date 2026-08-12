# Libs
import uuid  # UUID
from datetime import datetime  # Datetime
from pydantic import field_validator  # Pydantic
from typing import Any  # Typing

# Application
from base import BaseSchema  # Base
from enums.sync import SyncStatus  # Enum
from collectors.registry import PluginRegistry  # Collector Registry


class ReadMetricsSchema(BaseSchema):
    id: uuid.UUID
    collector: str
    sync_status: SyncStatus
    attempts: int
    last_attempt_at: datetime | None = None
    synced_at: datetime | None = None
    collected_at: datetime
    metrics: dict[str, Any]

    @field_validator("metrics", mode="before")
    @classmethod
    def validate_collector_metrics(cls, v: Any, info) -> dict[str, Any]:
        """
        Dynamically validates metrics payload against the collector's schema
        registered in PluginRegistry, if available.
        """
        collector_name = info.data.get("collector")
        if not collector_name:
            return v if isinstance(v, dict) else dict(v)

        collector_cls = PluginRegistry.get(collector_name)
        if collector_cls and hasattr(collector_cls, "schema_cls"):
            schema_cls = collector_cls.schema_cls
            if schema_cls:
                # If v is already a Pydantic model instance, dump to dict
                if isinstance(v, BaseSchema):
                    return v.model_dump(mode="json")
                # Validate raw dict against collector's schema
                validated_data = schema_cls.model_validate(v)
                return validated_data.model_dump(mode="json")

        return v if isinstance(v, dict) else dict(v)


class AckSchema(BaseSchema):
    metric_ids: list[uuid.UUID] = []
