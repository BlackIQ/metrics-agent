# Libs
import psutil  # PS Util

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import CollectorSchema  # Collector Schema


# Processor
class Collector(BaseCollector):
    name = "processor"
    default_interval = 5

    async def collect(self) -> CollectorSchema:
        total_logical = psutil.cpu_count(logical=True)
        total_physical = psutil.cpu_count(logical=False)
        total_usage = psutil.cpu_percent(interval=0)

        return CollectorSchema(
            count_logical=total_logical,
            count_physical=total_physical,
            percent=total_usage,
        )
