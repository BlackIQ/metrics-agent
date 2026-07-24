# Schema
from .schema import CollectorSchema

# PS Util
import psutil


def collect() -> CollectorSchema:
    total_logical = psutil.cpu_count(logical=True)
    total_physical = psutil.cpu_count(logical=False)
    total_usage = psutil.cpu_percent(interval=0)

    return CollectorSchema(
        count_logical=total_logical,
        count_physical=total_physical,
        percent=total_usage,
    )
