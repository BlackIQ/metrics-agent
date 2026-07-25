# Asyncio
import asyncio

# PS Util
import psutil

# Schema
from .schema import CollectorSchema

# Application
from services.save import save as save_metric  # Save Metrics


class Collector:
    name = "processor"

    interval = 5

    schema = CollectorSchema

    def collect(self) -> CollectorSchema:
        total_logical = psutil.cpu_count(logical=True)
        total_physical = psutil.cpu_count(logical=False)
        total_usage = psutil.cpu_percent(interval=0)

        return CollectorSchema(
            count_logical=total_logical,
            count_physical=total_physical,
            percent=total_usage,
        )

    async def save(self, metrics: CollectorSchema):
        await save_metric(self.name, metrics)

    async def run(self):
        while True:
            metrics = self.collect()

            await self.save(metrics)

            await asyncio.sleep(self.interval)
