# FastAPI
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

# Context
from contextlib import asynccontextmanager

# Asyncio
import asyncio

# Application
from core.logger import logger  # Logger
from core.settings import settings  # Settings
from routers import healthcheck, pull  # Routers
from collectors.registry import PluginRegistry  # Collector Registry
from services.manager import collector_manager  # Servie Manager
from services.cleanup import cleanup_old_metrics  # Service Cleanup


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing OpenHubble Agent lifecycle...")

    PluginRegistry.discover()

    default_config = [
        {"name": "system", "enabled": True, "options": {"interval": 5}},
        {"name": "processor", "enabled": True, "options": {"interval": 5}},
        {"name": "memory", "enabled": True, "options": {"interval": 5}},
        {"name": "swap", "enabled": True, "options": {"interval": 5}},
        {"name": "load", "enabled": True, "options": {"interval": 5}},
        {"name": "network", "enabled": True, "options": {"interval": 5}},
        {"name": "disk", "enabled": True, "options": {"interval": 10}},
        {"name": "io", "enabled": True, "options": {"interval": 5}},
    ]

    await collector_manager.reload_config(default_config)
    cleanup_task = asyncio.create_task(cleanup_old_metrics(retention_days=7))

    logger.info("OpenHubble Agent started successfully.")

    yield

    logger.info("Shutting down OpenHubble Agent...")

    collector_manager.stop_all()
    cleanup_task.cancel()


# Init FastAPI App
app = FastAPI(
    title="OpenHubble Agent",
    version=settings.project_version,
    summary="OpenHubble Agent API Documentation",
    description="API for retrieving various system and Docker metrics. Secure access requires an API key via the X-API-KEY header.",
    contact={
        "name": "OpenHubble Agent Team",
        "url": "https://openhubble.com/agent",
        "email": "agent@openhubble.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/OpenHubble/agent/blob/main/LICENSE",
    },
    openapi_tags=[
        {"name": "Health Check", "description": "Agent health checks"},
        {"name": "Pull", "description": "Pull metrics by cloud"},
    ],
    lifespan=lifespan,
)

# Use GZIP to compress data
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)


# Include Router
app.include_router(healthcheck.router, prefix="/api")
app.include_router(pull.router, prefix="/api")
