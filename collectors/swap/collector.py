# Asyncio
import asyncio

# PS Util
import psutil

# Schema
from .schema import CollectorSchema

# Application
from services.save import save as save_metric  # Save Metrics


class Collector:
    name = "swap"

    interval = 5

    schema = CollectorSchema

    def collect(self) -> CollectorSchema:
        swap = psutil.swap_memory()

        return CollectorSchema(
            used=swap.used,
            percent=swap.percent,
            free=swap.free,
            total=swap.total,
            sin=swap.sin,
            sout=swap.sout,
        )

    async def save(self, metrics: CollectorSchema):
        await save_metric(self.name, metrics)

    async def run(self):
        while True:
            metrics = self.collect()

            await self.save(metrics)

            await asyncio.sleep(self.interval)
