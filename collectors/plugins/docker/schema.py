# Libs
from typing import List  # Types

# Application
from base import BaseSchema


# Container Schema
class ContainerMetricsSchema(BaseSchema):
    id: str
    name: str
    image: str
    status: str
    state: str
    cpu_percent: float
    memory_usage_bytes: int
    memory_limit_bytes: int
    memory_percent: float


# Docker Schema
class DockerCollectorSchema(BaseSchema):
    total_containers: int
    running: int
    paused: int
    stopped: int
    containers: List[ContainerMetricsSchema]
