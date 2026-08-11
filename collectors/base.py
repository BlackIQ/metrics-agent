# Libs
from abc import ABC, abstractmethod  # Abstract
from typing import Any, Dict  # Types

# Application
from base import BaseSchema  # Base


# Base Collector
class BaseCollector(ABC):
    name: str
    default_interval: int = 15

    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or {}
        self.interval: int = self.config.get("interval", self.default_interval)
        self.enabled: bool = self.config.get("enabled", True)

    @abstractmethod
    async def collect(self) -> BaseSchema | Dict[str, Any]:
        pass
