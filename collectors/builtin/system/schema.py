# Application
from base import BaseSchema


# Collector Schema
class CollectorSchema(BaseSchema):
    hostname: str
    uptime: int
