# Application
from base import BaseModel


# Collector Schema
class CollectorSchema(BaseModel):
    hostname: str
    uptime: int
