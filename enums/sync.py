# Enum
from enum import StrEnum


# Sync Status Enum
class SyncStatus(StrEnum):
    pending = "pending"
    processing = "processing"
    synced = "synced"
    failed = "failed"
