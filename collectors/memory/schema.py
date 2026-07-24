# Application
from base import BaseModel


# Collector Schema
class CollectorSchema(BaseModel):
    total: int
    available: int
    percent: float
    used: int
    free: int
    active: int
    inactive: int
    wired: int
