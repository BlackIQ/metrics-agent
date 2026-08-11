# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
