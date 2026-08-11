# Libs
from typing import Dict  # Types

# Collector Schema
from base import BaseSchema


# Interface Schema
class InterfaceMetricsSchema(BaseSchema):
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    errin: int
    errout: int
    dropin: int
    dropout: int
    rx_speed_bytes_sec: float = 0.0
    tx_speed_bytes_sec: float = 0.0


# Collector Schema
class NetworkCollectorSchema(BaseSchema):
    total_bytes_sent: int
    total_bytes_recv: int
    rx_speed_bytes_sec: float = 0.0
    tx_speed_bytes_sec: float = 0.0
    active_connections: int
    sockets_by_state: Dict[str, int]
    interfaces: Dict[str, InterfaceMetricsSchema]
