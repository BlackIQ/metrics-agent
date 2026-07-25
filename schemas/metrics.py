# Application
from base import BaseModel

# Collector schemas
from collectors.system.schema import CollectorSchema as SystemSchema
from collectors.load.schema import CollectorSchema as LoadSchema
from collectors.memory.schema import CollectorSchema as MemorySchema
from collectors.swap.schema import CollectorSchema as SwapSchema
from collectors.cpu.schema import CollectorSchema as CPUSchema


class MetricsSchema(BaseModel):
    system: SystemSchema
    load: LoadSchema
    memory: MemorySchema
    swap: SwapSchema
    cpu: CPUSchema
