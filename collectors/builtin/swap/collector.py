# Libs
import psutil  # PS Util

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import CollectorSchema  # Collector Schema


# Swap
class Collector(BaseCollector):
    name = "swap"
    default_interval = 5
    schema_cls = CollectorSchema

    async def collect(self) -> CollectorSchema:
        swap = psutil.swap_memory()

        return CollectorSchema(
            used=swap.used,
            percent=swap.percent,
            free=swap.free,
            total=swap.total,
            sin=swap.sin,
            sout=swap.sout,
        )
