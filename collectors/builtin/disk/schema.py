# Libs
from typing import Dict  # Types

# Collector Schema
from base import BaseSchema


# Mount Schema
class MountUsageSchema(BaseSchema):
    device: str
    fstype: str
    total_bytes: int
    used_bytes: int
    free_bytes: int
    percent: float
    total_inodes: int = 0
    used_inodes: int = 0
    free_inodes: int = 0
    inodes_percent: float = 0.0


# Collector Schema
class DiskCollectorSchema(BaseSchema):
    mounts: Dict[str, MountUsageSchema]
