# Libs
import os  # OS

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import CollectorSchema  # Collector Schema


# Load
class Collector(BaseCollector):
    name = "load"
    default_interval = 5

    async def collect(self) -> CollectorSchema:
        min_1, min_3, min_15 = os.getloadavg()
        return CollectorSchema(
            min_1=min_1,
            min_3=min_3,
            min_15=min_15,
        )
