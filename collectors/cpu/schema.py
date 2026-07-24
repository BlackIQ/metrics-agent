# Application
from base import BaseModel


# Collector Schema
class CollectorSchema(BaseModel):
    count_logical: int | None
    count_physical: int | None
    percent: float
