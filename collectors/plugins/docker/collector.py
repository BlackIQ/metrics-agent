# Libs
import docker # Docker
import asyncio # Asyncio
from typing import Dict, Any # Types

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import DockerCollectorSchema, ContainerMetricsSchema # Collector Schemas


class Collector(BaseCollector):
    name = "docker"
    default_interval = 10
    schema_cls = DockerCollectorSchema

    def _calculate_cpu_percent(self, stats: Dict[str, Any]) -> float:
        try:
            cpu_stats = stats.get("cpu_stats", {})
            precpu_stats = stats.get("precpu_stats", {})

            cpu_delta = (
                cpu_stats.get("cpu_usage", {}).get("total_usage", 0)
                - precpu_stats.get("cpu_usage", {}).get("total_usage", 0)
            )
            system_delta = (
                cpu_stats.get("system_cpu_usage", 0)
                - precpu_stats.get("system_cpu_usage", 0)
            )

            online_cpus = cpu_stats.get("online_cpus") or len(
                cpu_stats.get("cpu_usage", {}).get("percpu_usage", [1])
            )

            if system_delta > 0.0 and cpu_delta > 0.0:
                return round((cpu_delta / system_delta) * online_cpus * 100.0, 2)
        except (KeyError, ZeroDivisionError, TypeError):
            pass
        return 0.0

    def _collect_sync((self) -> DockerCollectorSchema:
        client = docker.DockerClient(base_url=self.config.get("socket_path", "unix://var/run/docker.sock"))

        try:
            containers = client.containers.list(all=True)
            total_containers = len(containers)
            running = 0
            paused = 0
            stopped = 0

            container_list = []

            for container in containers:
                status = container.status.lower()
                if status == "running":
                    running += 1
                elif status == "paused":
                    paused += 1
                else:
                    stopped += 1

                cpu_pct = 0.0
                mem_usage = 0
                mem_limit = 0
                mem_pct = 0.0

                if status == "running":
                    try:
                        stats = container.stats(stream=False)
                        
                        cpu_pct = self._calculate_cpu_percent(stats)

                        mem_stats = stats.get("memory_stats", {})
                        mem_usage = mem_stats.get("usage", 0)
                        mem_limit = mem_stats.get("limit", 1)
                        if mem_limit > 0:
                            mem_pct = round((mem_usage / mem_limit) * 100.0, 2)
                    except Exception:
                        pass

                container_list.append(
                    ContainerMetricsSchema(
                        id=container.short_id,
                        name=container.name.lstrip("/"),
                        image=container.image.tags[0] if container.image.tags else container.image.id[:12],
                        status=container.status,
                        state=container.attrs.get("State", {}).get("Status", "unknown"),
                        cpu_percent=cpu_pct,
                        memory_usage_bytes=mem_usage,
                        memory_limit_bytes=mem_limit,
                        memory_percent=mem_pct,
                    )
                )

            return DockerCollectorSchema(
                total_containers=total_containers,
                running=running,
                paused=paused,
                stopped=stopped,
                containers=container_list,
            )
        finally:
            client.close()

    async def collect(self) -> DockerCollectorSchema:
        return await asyncio.to_thread(self._collect_sync)