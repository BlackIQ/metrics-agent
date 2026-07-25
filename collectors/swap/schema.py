# Application
from base import BaseSchema


# Collector Schema
class CollectorSchema(BaseSchema):
    total: int
    used: int
    free: int
    percent: float
    sin: int
    sout: int
