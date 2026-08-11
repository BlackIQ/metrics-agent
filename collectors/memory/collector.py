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
            available=memory.available,
            percent=memory.percent,
            used=memory.used,
            free=memory.free,
            active=getattr(memory, "active", 0),
            inactive=getattr(memory, "inactive", 0),
            wired=getattr(memory, "wired", 0),
        )

    async def save(self, metrics: CollectorSchema):
        await save_metric(self.name, metrics)

    async def run(self):
        while True:
            metrics = self.collect()

            await self.save(metrics)

            await asyncio.sleep(self.interval)
