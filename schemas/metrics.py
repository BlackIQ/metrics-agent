# Application
from base import BaseSchema

# Collector schemas
from collectors.system.schema import CollectorSchema as SystemSchema
from collectors.load.schema import CollectorSchema as LoadSchema
from collectors.memory.schema import CollectorSchema as MemorySchema
from collectors.swap.schema import CollectorSchema as SwapSchema
from collectors.processor.schema import CollectorSchema as ProcessorSchema


class MetricsSchema(BaseSchema):
    system: SystemSchema
    load: LoadSchema
    memory: MemorySchema
    swap: SwapSchema
    cpu: ProcessorSchema
