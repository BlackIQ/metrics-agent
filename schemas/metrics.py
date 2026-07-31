# UUID
import uuid

# Datetime
from datetime import datetime

# Application
from base import BaseSchema  # Base
from enums.sync import SyncStatus

# Collector schemas
from collectors.system.schema import CollectorSchema as SystemSchema
from collectors.load.schema import CollectorSchema as LoadSchema
from collectors.memory.schema import CollectorSchema as MemorySchema
from collectors.swap.schema import CollectorSchema as SwapSchema
from collectors.processor.schema import CollectorSchema as ProcessorSchema


class MetricDataSchema(BaseSchema):
    system: SystemSchema
    load: LoadSchema
    memory: MemorySchema
    swap: SwapSchema
    cpu: ProcessorSchema


class ReadMetricsSchema(BaseSchema):
    id: uuid.UUID
    collector: str
    sync_status: SyncStatus
    attempts: int
    last_attempt_at: datetime | None = None
    synced_at: datetime | None = None
    collected_at: datetime
    # metrics: MetricDataSchema
