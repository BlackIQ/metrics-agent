# Libs
import importlib  # Import lib
import pkgutil  # Package Util
import inspect  # Inspect lib
from typing import Dict, Type  # Types

# Application
from collectors.base import BaseCollector  # Base


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
                print(f"Failed to load collector module {module_name}: {e}")

    @classmethod
    def get(cls, name: str) -> Type[BaseCollector] | None:
        return cls._registry.get(name)

    @classmethod
    def list_available(cls) -> list[str]:
        return list(cls._registry.keys())
