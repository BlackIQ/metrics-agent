# Schema
from .schema import CollectorSchema

# PS Util
import psutil


def collect() -> CollectorSchema:
    swap = psutil.swap_memory()

    return CollectorSchema(
        used=swap.used,
        percent=swap.percent,
        free=swap.free,
        total=swap.total,
        sin=swap.sin,
        sout=swap.sout,
    )
