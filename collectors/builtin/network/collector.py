# Libs
import psutil  # PS Util
import time  # Time
from typing import Dict, Any  # Types

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import NetworkCollectorSchema, InterfaceMetricsSchema  # Collector Schemas


# Network
class Collector(BaseCollector):
    name = "network"
    default_interval = 5
    schema_cls = NetworkCollectorSchema

    def __init__(self, config: Dict[str, Any] | None = None):
        super().__init__(config)
        self._last_time: float | None = None
        self._last_io: Any | None = None
        self._last_interface_io: Dict[str, Any] = {}

    async def collect(self) -> NetworkCollectorSchema:
        now = time.time()
        current_io = psutil.net_io_counters()
        current_if_io = psutil.net_io_counters(pernic=True)

        rx_rate = 0.0
        tx_rate = 0.0

        if self._last_time and self._last_io:
            dt = now - self._last_time
            if dt > 0:
                rx_rate = round(
                    (current_io.bytes_recv - self._last_io.bytes_recv) / dt, 2
                )
                tx_rate = round(
                    (current_io.bytes_sent - self._last_io.bytes_sent) / dt, 2
                )

        interface_map: Dict[str, InterfaceMetricsSchema] = {}
        for iface_name, io in current_if_io.items():
            iface_rx_rate = 0.0
            iface_tx_rate = 0.0

            if self._last_time and iface_name in self._last_interface_io:
                dt = now - self._last_time
                if dt > 0:
                    prev_if = self._last_interface_io[iface_name]
                    iface_rx_rate = round((io.bytes_recv - prev_if.bytes_recv) / dt, 2)
                    iface_tx_rate = round((io.bytes_sent - prev_if.bytes_sent) / dt, 2)

            interface_map[iface_name] = InterfaceMetricsSchema(
                bytes_sent=io.bytes_sent,
                bytes_recv=io.bytes_recv,
                packets_sent=io.packets_sent,
                packets_recv=io.packets_recv,
                errin=io.errin,
                errout=io.errout,
                dropin=io.dropin,
                dropout=io.dropout,
                rx_speed_bytes_sec=iface_rx_rate,
                tx_speed_bytes_sec=iface_tx_rate,
            )

        sockets_by_state: Dict[str, int] = {}
        active_conns = 0
        try:
            connections = psutil.net_connections(kind="inet")
            active_conns = len(connections)
            for conn in connections:
                st = conn.status
                sockets_by_state[st] = sockets_by_state.get(st, 0) + 1
        except Exception:
            pass

        self._last_time = now
        self._last_io = current_io
        self._last_interface_io = current_if_io

        return NetworkCollectorSchema(
            total_bytes_sent=current_io.bytes_sent,
            total_bytes_recv=current_io.bytes_recv,
            rx_speed_bytes_sec=rx_rate,
            tx_speed_bytes_sec=tx_rate,
            active_connections=active_conns,
            sockets_by_state=sockets_by_state,
            interfaces=interface_map,
        )
