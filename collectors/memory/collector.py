# Asyncio
import asyncio

# PS Util
import psutil

# Schema
from .schema import CollectorSchema

# Application
from services.save import save as save_metric  # Save Metrics


class Collector:
    name = "memory"

    interval = 5

    schema = CollectorSchema

    def collect(self) -> CollectorSchema:
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

    async def save(self, metrics: CollectorSchema):
        await save_metric(self.name, metrics)

    async def run(self):
        while True:
            metrics = self.collect()

            await self.save(metrics)

            await asyncio.sleep(self.interval)
