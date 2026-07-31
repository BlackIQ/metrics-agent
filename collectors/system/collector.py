# Asyncio
import asyncio

# Time
import time
import psutil

# Schema
from .schema import CollectorSchema

# Application
from core.settings import settings  # Settings
from services.save import save as save_metric  # Save Metrics


class Collector:
    name = "system"

    interval = 5

    schema = CollectorSchema

    def collect(self) -> CollectorSchema:
        return CollectorSchema(
            hostname=settings.hostname,
            uptime=int(time.time() - psutil.boot_time()),
        )

    async def save(self, metrics: CollectorSchema):
        await save_metric(self.name, metrics)

    async def run(self):
        while True:
            metrics = self.collect()

            await self.save(metrics)

            await asyncio.sleep(self.interval)
