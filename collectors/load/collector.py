# Schema
from .schema import CollectorSchema

# OS
import os


def collect() -> CollectorSchema:
    min_1, min_3, min_15 = os.getloadavg()

    return CollectorSchema(
        min_1=min_1,
        min_3=min_3,
        min_15=min_15,
    )
