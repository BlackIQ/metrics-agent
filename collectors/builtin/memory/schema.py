# Application
from base import BaseSchema


# Collector Schema
class CollectorSchema(BaseSchema):
    total: int
    available: int
    percent: float
    used: int
    free: int
    active: int = 0
    inactive: int = 0
    wired: int = 0
