---
id: ARCH-config-manager
title: "Configuration Manager"
type: component
layer: application
owner: @vibe-team
version: v1
status: current
created: 2025-06-08
updated: 2025-06-08
tags: [configuration, json, pydantic]
depends_on: [ARCH-data-models]
referenced_by: []
---
## Context
The Configuration Manager is responsible for loading, validating, and providing access to all external configurations required by the application. This centralization ensures that configuration logic is not scattered throughout the codebase.

## Structure
*   **Primary File:** `src/vibe_python/config.py`
*   **Key Responsibilities:**
    *   **Environment Variables:** Loads the `.env` file to retrieve sensitive data like database connection strings and email credentials.
    *   **Robot Definitions:** Scans the `configs/robots.d/` directory for all `*.json` files.
    *   **Validation:** Uses Pydantic models (defined in `ARCH-data-models`) to parse and validate the structure and data types of each robot configuration file. This prevents malformed configurations from crashing the application at runtime.
    *   **Consolidation:** Aggregates all valid robot configurations into a single, easily accessible in-memory data structure for other components to use.
    *   **Error Handling:** Raises a clear error on startup if duplicate `robot_name` values are found across different configuration files.

## Behavior
*   On application startup, the Orchestrator initializes the Configuration Manager.
*   The manager loads all configurations into memory. If any validation fails, the application startup is halted with an error message.
*   Other components, like the `Scheduler` and `Executor`, request configuration data (e.g., a specific robot's schedule or action list) from the Configuration Manager.
*   The configuration is loaded once at startup. A service restart is required to apply any changes made to the configuration files.

## Evolution
### Planned
*   No immediate changes are planned. Future enhancements might include support for hot-reloading configurations without a service restart.

### Historical
*   **v1:** Initial design. Supports loading from a `.env` file and a `configs/robots.d/` directory. Includes robust validation using Pydantic. 