# Asyncio
import asyncio

# Collectors
from collectors.system.collector import Collector as SystemCollector
from collectors.load.collector import Collector as LoadCollector
from collectors.processor.collector import Collector as ProcessorCollector
from collectors.memory.collector import Collector as MemoryCollector
from collectors.swap.collector import Collector as SwapCollector


async def start_collectors():
    collectors = [
        SystemCollector(),
        ProcessorCollector(),
        MemoryCollector(),
        SwapCollector(),
        LoadCollector(),
    ]

    # Run all collector loops concurrently
    await asyncio.gather(*(collector.run() for collector in collectors))
