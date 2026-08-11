# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-08-12

### Added

- Introduced the new **Runtime Monitoring Agent** architecture.
- Introduced a **plugin-based architecture** for runtime monitoring.
- Added a **Plugin Registry** for automatic plugin discovery and management.
- Converted existing built-in monitoring functionality into plugins.
- Added built-in **Disk** plugin.
- Added built-in **I/O** plugin.
- Added built-in **Network** plugin.
- Added **PostgreSQL** plugin.
- Added **Docker** plugin.
- Added support for activating optional plugins through the OpenHubble CLI.
- Added a complete project-wide logging system.
- Added persistent agent logs under `/var/log/openhubble-agent`.

### Changed

- Reworked data collection architecture around a centralized `manager.py`.
- Moved metric collection and orchestration away from the previous `run.py`, `save.py`, and related boilerplate.
- Reorganized the Agent around the new plugin and registry architecture.
- Simplified the internal data collection pipeline.
- Improved plugin discovery and lifecycle management.
- Improved CLI plugin management workflow.

### Improved

- Significantly improved Agent performance.
- Reduced unnecessary boilerplate and duplicated logic.
- Improved asynchronous execution and metric collection.
- Improved overall code organization and maintainability.
- Improved OpenHubble CLI speed and usability.
- Improved CLI reliability.
- Improved logging and operational visibility.

### Fixed

- Fixed an issue preventing the OpenHubble CLI from working correctly.
- Fixed issues in the previous plugin/command management workflow.

### Removed

- Removed legacy hard-coded metric collection architecture.
- Removed unnecessary collection boilerplate previously distributed across multiple modules.

### Architecture

OpenHubble Agent is now a **Runtime Monitoring Agent** built around a discoverable plugin architecture.

The Agent can discover and manage monitoring plugins through its Plugin Registry, allowing monitoring capabilities to be added without modifying the core Agent.

Built-in plugins now include:

- Host
- Memory
- CPU
- Load
- Swap
- Disk
- I/O
- Network
- PostgreSQL
- Docker

## [2.20.0] - 2026-08-11

### Added

- Added fallback values for unavailable platform-specific metrics.
- Added metrics cleanup service for removing old metrics.
- Added metrics acknowledgment (ACK) endpoint.
- Added support for marking metrics as synchronized using UUIDs.
- Added new database migrations for metrics synchronization and persistence.

### Changed

- Improved asynchronous metric collection.
- Improved asynchronous metric persistence.
- Improved metrics synchronization workflow.
- Improved handling of platform-specific metric availability.

### Improved

- Optimized metrics pull endpoint.
- Improved database queries and metric retrieval performance.
- Improved reliability of metric collection.
- Improved overall metrics processing and persistence.

## [2.19.1] - 2026-08-11

### Fixed

- Fixed an issue where OpenHubble Agent settings were not loaded correctly.
- Improved configuration initialization and settings availability during application startup.

## [2.19.0] - 2026-07-31

### Added

- SQLAlchemy ORM integration
- Alembic database migrations
- SQLite persistent storage
- Pydantic request validation
- Pydantic response validation
- Pydantic Settings configuration management
- Initial collectors architecture
- Host metrics collection
- FastAPI Lifespan support
- Improved async infrastructure

### Changed

- Migrated configuration from `.ini` to `.env`
- Switched project management to `uv`
- Updated installation workflow
- Updated `install.sh`
- Added improved `update.sh`
- Added improved `uninstall.sh`
- Updated systemd service configuration
- Improved TOML configuration parsing

### Improved

- API Key middleware reliability
- IP middleware
- Swagger documentation
- ReDoc documentation
- OpenAPI documentation
- Overall API validation
- Internal architecture and maintainability

## [2.18.10] - 2025-03-08

### Added

- API KEY implementation
- API KEY middleware
- FastAPI docs

### Improved

- New version validation in update
- NetIO/BlockIO Delta value
- Secure communication

### Removed

- Git-based updates

## [2.10.4] - 2025-02-01

### Added

- Check new version

### Improved

- Work on performance
- Compression data
- Better logging
- Parallelized metrics collection

## [2.3.1] - 2025-01-29

### Refactored

- Migrated to FastAPI

### Added

- Introduced `agent.toml` configuration file

### Fixed

- Resolved two security vulnerabilities
