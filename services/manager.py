# Libs
import asyncio  # Asyncio
from typing import Dict, Any  # Types

# Application
from collectors.registry import PluginRegistry  # Collector Registry
from services.save import save as save_metric  # Save Service


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
            print(f"[Manager] Stopping collector task: {name}")
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
                    print(
                        f"[Manager] Started collector task: '{name}' (interval: {inst.interval}s)"
                    )
                else:
                    print(
                        f"[Manager] WARNING: Collector '{name}' requested in config but not found in PluginRegistry!"
                    )

    async def _run_collector_loop(self, collector):
        print(f"[Collector:{collector.name}] Loop started.")
        while True:
            try:
                metrics = await collector.collect()
                await save_metric(collector.name, metrics)
            except asyncio.CancelledError:
                print(f"[Collector:{collector.name}] Task cancelled.")
                break
            except Exception as e:
                print(f"[Collector:{collector.name}] Error collecting metrics: {e}")

            # Fallback to default 5 seconds if interval isn't set
            sleep_time = getattr(collector, "interval", 5) or 5
            await asyncio.sleep(sleep_time)

    def stop_all(self):
        for name, task in self.tasks.items():
            task.cancel()
        self.tasks.clear()


collector_manager = CollectorManager()
