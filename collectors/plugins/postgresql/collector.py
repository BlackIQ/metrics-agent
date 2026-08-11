# Libs
import asyncpg  # Async PostgreSQL

# Application
from collectors.base import BaseCollector  # Base Collector
from .schema import PostgresSchema  # Collector Schema


# PostgreSQL
class Collector(BaseCollector):
    name = "postgresql"
    default_interval = 10

    async def collect(self) -> PostgresSchema:
        dsn = self.config.get(
            "dsn", "postgresql://postgres:postgres@localhost:5432/postgres"
        )

        conn = await asyncpg.connect(dsn, timeout=5)

        try:
            active = await conn.fetchval(
                "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"
            )
            idle = await conn.fetchval(
                "SELECT count(*) FROM pg_stat_activity WHERE state = 'idle';"
            )
            stats = await conn.fetchrow(
                "SELECT sum(xact_commit) as commits, sum(xact_rollback) as rollbacks FROM pg_stat_database;"
            )

            return PostgresSchema(
                active_connections=active or 0,
                idle_connections=idle or 0,
                total_commits=stats["commits"] or 0 if stats else 0,
                total_rollbacks=stats["rollbacks"] or 0 if stats else 0,
            )

        finally:
            await conn.close()
