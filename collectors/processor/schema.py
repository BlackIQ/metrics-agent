# Application
from base import BaseSchema


# Collector Schema
class CollectorSchema(BaseSchema):
    count_logical: int | None
    count_physical: int | None
    percent: float
