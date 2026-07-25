# Asyncio
import asyncio

# OS
import os

# Schema
from .schema import CollectorSchema

# Application
from services.save import save as save_metric  # Save Metrics


class Collector:
    name = "load"

    interval = 5

    schema = CollectorSchema

    def collect(self) -> CollectorSchema:
        min_1, min_3, min_15 = os.getloadavg()

        return CollectorSchema(
            min_1=min_1,
            min_3=min_3,
            min_15=min_15,
        )

    async def save(self, metrics: CollectorSchema):
        await save_metric(self.name, metrics)

    async def run(self):
        while True:
            metrics = self.collect()

            await self.save(metrics)

            await asyncio.sleep(self.interval)
