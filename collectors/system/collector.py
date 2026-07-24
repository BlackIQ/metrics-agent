# Schema
from .schema import CollectorSchema

# Application
from core.settings import settings


def collect() -> CollectorSchema:
    return CollectorSchema(
        hostname=settings.hostname,
        uptime=0,
    )
