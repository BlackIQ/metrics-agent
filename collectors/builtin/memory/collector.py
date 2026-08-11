# Libs
import psutil  # PS Util

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import CollectorSchema  # Collector Schema


# Memory
class Collector(BaseCollector):
    name = "memory"
    default_interval = 5

    async def collect(self) -> CollectorSchema:
        memory = psutil.virtual_memory()

        return CollectorSchema(
            total=memory.total,
            available=memory.available,
            percent=memory.percent,
            used=memory.used,
            free=memory.free,
            active=getattr(memory, "active", 0),
            inactive=getattr(memory, "inactive", 0),
            wired=getattr(memory, "wired", 0),
        )
