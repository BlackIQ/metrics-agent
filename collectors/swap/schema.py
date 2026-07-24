# Application
from base import BaseModel


# Collector Schema
class CollectorSchema(BaseModel):
    total: int
    used: int
    free: int
    percent: float
    sin: int
    sout: int
