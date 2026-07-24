# Schema
from .schema import CollectorSchema

# PS Util
import psutil


def collect() -> CollectorSchema:
    memory = psutil.virtual_memory()

    return CollectorSchema(
        total=memory.total,
        active=memory.active,
        inactive=memory.inactive,
        free=memory.free,
        used=memory.used,
        available=memory.available,
        percent=memory.percent,
        wired=memory.wired,
    )
