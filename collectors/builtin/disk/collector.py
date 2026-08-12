# Libs
import psutil  # PS Util
import os  # OS
from typing import Dict  # Types

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import DiskCollectorSchema, MountUsageSchema  # Collector Schemas


# Disk
class Collector(BaseCollector):
    name = "disk"
    default_interval = 5
    schema_cls = DiskCollectorSchema

    IGNORED_FSTYPES = {
        "tmpfs",
        "devtmpfs",
        "devfs",
        "sysfs",
        "proc",
        "squashfs",
        "overlay",
    }

    async def collect(self) -> DiskCollectorSchema:
        mounts: Dict[str, MountUsageSchema] = {}

        for part in psutil.disk_partitions(all=False):
            if part.fstype.lower() in self.IGNORED_FSTYPES:
                continue

            try:
                usage = psutil.disk_usage(part.mountpoint)
            except (PermissionError, FileNotFoundError):
                continue

            total_inodes = 0
            used_inodes = 0
            free_inodes = 0
            inodes_pct = 0.0

            if hasattr(os, "statvfs"):
                try:
                    vfs = os.statvfs(part.mountpoint)
                    total_inodes = vfs.f_files
                    free_inodes = vfs.f_ffree
                    used_inodes = total_inodes - free_inodes
                    if total_inodes > 0:
                        inodes_pct = round((used_inodes / total_inodes) * 100.0, 2)
                except Exception:
                    pass

            mounts[part.mountpoint] = MountUsageSchema(
                device=part.device,
                fstype=part.fstype,
                total_bytes=usage.total,
                used_bytes=usage.used,
                free_bytes=usage.free,
                percent=usage.percent,
                total_inodes=total_inodes,
                used_inodes=used_inodes,
                free_inodes=free_inodes,
                inodes_percent=inodes_pct,
            )

        return DiskCollectorSchema(mounts=mounts)
