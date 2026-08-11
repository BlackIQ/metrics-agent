# Libs
import psutil  # PS Util
import time  # Time

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import CollectorSchema  # Collector Schema
from core.settings import settings


# System
class Collector(BaseCollector):
    name = "system"
    default_interval = 5

    async def collect(self) -> CollectorSchema:
        return CollectorSchema(
            hostname=settings.hostname,
            uptime=int(time.time() - psutil.boot_time()),
        )
