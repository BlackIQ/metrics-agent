# Enum
from enum import StrEnum


# Sync Status Enum
class SyncStatus(StrEnum):
    pending = "pending"
    sending = "sending"
    synced = "synced"
    failed = "failed"
