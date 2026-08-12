# Libs
import importlib  # Import lib
import pkgutil  # Package Util
import inspect  # Inspect lib
from typing import Dict, Type, Any  # Types

# Application
from core.logger import get_logger  # Logger
from collectors.base import BaseCollector  # Base

# Logger (Registry)
logger = get_logger("registry")


# Plugin Registry
class PluginRegistry:
    _registry: Dict[str, Type[BaseCollector]] = {}

    @classmethod
    def discover(cls):
        import collectors

        cls._registry.clear()

        package_path = collectors.__path__
        prefix = collectors.__name__ + "."

        for _, module_name, is_pkg in pkgutil.walk_packages(package_path, prefix):
            try:
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (
                        issubclass(obj, BaseCollector)
                        and obj is not BaseCollector
                        and hasattr(obj, "name")
                    ):
                        cls._registry[obj.name] = obj
            except Exception as e:
                logger.error(f"Failed to load collector module '{module_name}': {e}")

        logger.info(f"Discovered collectors: {list(cls._registry.keys())}")

    @classmethod
    def get(cls, name: str) -> Type[BaseCollector] | None:
        return cls._registry.get(name)

    @classmethod
    def list_available(cls) -> list[str]:
        return list(cls._registry.keys())

    @classmethod
    def get_all_schemas(cls) -> dict[str, Any]:
        schemas = {}
        for name, collector_cls in cls._registry.items():
            if hasattr(collector_cls, "schema_cls") and collector_cls.schema_cls:
                schemas[name] = collector_cls.schema_cls

        return schemas
