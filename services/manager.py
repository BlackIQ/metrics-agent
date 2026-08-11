# Libs
import asyncio  # Asyncio
from typing import Dict, Any  # Types

# Application
from core.logger import get_logger  # Logger
from collectors.registry import PluginRegistry  # Collector Registry
from services.save import save as save_metric  # Save Service

# Logger (Manager)
logger = get_logger("manager")


class CollectorManager:
    def __init__(self):
        self.tasks: Dict[str, asyncio.Task] = {}
        self.configs: Dict[str, Dict[str, Any]] = {}

    async def reload_config(self, active_configs: list[dict]):
        desired_names = {
            cfg["name"] for cfg in active_configs if cfg.get("enabled", True)
        }
        current_names = set(self.tasks.keys())

        # Stop disabled or removed collectors
        for name in current_names - desired_names:
            logger.info(f"Stopping collector task: {name}")

            self.tasks[name].cancel()
            del self.tasks[name]
            del self.configs[name]

        for cfg in active_configs:
            name = cfg["name"]
            if not cfg.get("enabled", True):
                continue

            if name not in self.tasks or self.configs.get(name) != cfg:
                if name in self.tasks:
                    self.tasks[name].cancel()

                collector_cls = PluginRegistry.get(name)
                if collector_cls:
                    # Pass options directly into the collector instance
                    options = cfg.get("options", {})
                    inst = collector_cls(options)

                    task = asyncio.create_task(self._run_collector_loop(inst))
                    self.tasks[name] = task
                    self.configs[name] = cfg

                    logger.info(
                        f"Started collector task: '{name}' (interval: {inst.interval}s)"
                    )
                else:
                    logger.warning(
                        f"Collector '{name}' requested in config but not found in PluginRegistry!"
                    )

    async def _run_collector_loop(self, collector):
        logger.debug(f"[{collector.name}] Collector loop started.")

        while True:
            try:
                metrics = await collector.collect()
                await save_metric(collector.name, metrics)
            except asyncio.CancelledError:
                logger.info(f"[{collector.name}] Collector task cancelled.")
                break
            except Exception as e:
                logger.error(
                    f"[{collector.name}] Error collecting metrics: {e}",
                    exc_info=True,
                )

            sleep_time = getattr(collector, "interval", 5) or 5
            await asyncio.sleep(sleep_time)

    def stop_all(self):
        for name, task in self.tasks.items():
            task.cancel()
        self.tasks.clear()


collector_manager = CollectorManager()
