# Libs
import psutil  # PS Util
import time  # Time
from typing import Dict, Any  # Types

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import IOCollectorSchema, DriveIOSchema  # Collector Schemas


# IO
class Collector(BaseCollector):
    name = "io"
    default_interval = 5

    def __init__(self, config: Dict[str, Any] | None = None):
        super().__init__(config)
        self._last_time: float | None = None
        self._last_disk_io: Dict[str, Any] = {}

    async def collect(self) -> IOCollectorSchema:
        now = time.time()
        current_io = psutil.disk_io_counters(perdisk=True)

        drives: Dict[str, DriveIOSchema] = {}
        total_rx_sec = 0.0
        total_wx_sec = 0.0

        if current_io:
            for disk_name, io in current_io.items():
                read_sec = 0.0
                write_sec = 0.0
                iops_r = 0.0
                iops_w = 0.0

                if self._last_time and disk_name in self._last_disk_io:
                    dt = now - self._last_time
                    if dt > 0:
                        prev = self._last_disk_io[disk_name]
                        read_sec = round((io.read_bytes - prev.read_bytes) / dt, 2)
                        write_sec = round((io.write_bytes - prev.write_bytes) / dt, 2)
                        iops_r = round((io.read_count - prev.read_count) / dt, 2)
                        iops_w = round((io.write_count - prev.write_count) / dt, 2)

                total_rx_sec += read_sec
                total_wx_sec += write_sec

                drives[disk_name] = DriveIOSchema(
                    read_count=io.read_count,
                    write_count=io.write_count,
                    read_bytes=io.read_bytes,
                    write_bytes=io.write_bytes,
                    read_time_ms=io.read_time,
                    write_time_ms=io.write_time,
                    read_bytes_sec=read_sec,
                    write_bytes_sec=write_sec,
                    iops_read=iops_r,
                    iops_write=iops_w,
                )

        self._last_time = now
        self._last_disk_io = current_io or {}

        return IOCollectorSchema(
            total_read_bytes_sec=round(total_rx_sec, 2),
            total_write_bytes_sec=round(total_wx_sec, 2),
            drives=drives,
        )
