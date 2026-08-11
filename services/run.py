# Asyncio
import asyncio

# Collectors
from collectors.builtin.system.collector import Collector as SystemCollector
from collectors.builtin.load.collector import Collector as LoadCollector
from collectors.builtin.processor.collector import Collector as ProcessorCollector
from collectors.builtin.memory.collector import Collector as MemoryCollector
from collectors.builtin.swap.collector import Collector as SwapCollector


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
