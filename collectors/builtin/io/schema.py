# Libs
from typing import Dict  # Types

# Collector Schema
from base import BaseSchema


# Drive IO Schema
class DriveIOSchema(BaseSchema):
    read_count: int
    write_count: int
    read_bytes: int
    write_bytes: int
    read_time_ms: int
    write_time_ms: int
    read_bytes_sec: float = 0.0
    write_bytes_sec: float = 0.0
    iops_read: float = 0.0
    iops_write: float = 0.0


# Collector Schema
class IOCollectorSchema(BaseSchema):
    total_read_bytes_sec: float = 0.0
    total_write_bytes_sec: float = 0.0
    drives: Dict[str, DriveIOSchema]
