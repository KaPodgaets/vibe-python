---
id: ARCH-data-models
title: "Application Data Models"
type: data_model
layer: domain
owner: @vibe-team
version: v1
status: current
created: 2025-06-08
updated: 2025-06-08
tags: [pydantic, sqlalchemy, schema]
depends_on: []
referenced_by: []
---
## Context
This document defines the core data structures for the application, including configuration file schemas and database table schemas. These models ensure data consistency and validation across the system. They are intended to be centralized in `src/vibe_python/models.py`.

## Structure

### Configuration Models (Pydantic)
These models define the expected structure of the robot `.json` files.

**`Robot` Model:**
```json
{
  "robot_name": "string (unique)",
  "description": "string",
  "enabled": "boolean",
  "schedule": {
    "type": "string ('cron')",
    "expression": "string (cron expression)"
  },
  "on_failure": {
    "retries": "integer (e.g., 2)",
    "delay_seconds": "integer (e.g., 300)"
  },
  "actions": "[Action]"
}
```
**`Action` Model:**
*   `type`: (e.g., `click`, `write`, `move_to`, `screenshot`)
*   `params`: A dictionary of parameters specific to the action type.
*   `description`: A human-readable string.

### Database Models (SQLAlchemy)
These models define the database schema for persisting operational data in MS SQL Server.

**`TaskRuns` Table:**
*   `id` (PK, int, auto-increment)
*   `robot_name` (varchar)
*   `status` (varchar: 'Pending', 'Running', 'Success', 'Failed')
*   `retry_count` (int, default 0)
*   `created_at`, `started_at`, `completed_at` (datetime)
*   `result_message` (varchar)

**`LogEntries` Table:**
*   `id` (PK, int, auto-increment)
*   `task_run_id` (FK to TaskRuns.id)
*   `timestamp` (datetime)
*   `level` (varchar: 'INFO', 'WARN', 'ERROR')
*   `message` (varchar)
*   `screenshot_path` (varchar, nullable)

## Behavior
*   Pydantic models are used by the `Configuration Manager` to validate robot JSON files upon loading.
*   SQLAlchemy models are used by the `Data Access Layer (DAL)` to perform all database operations (CRUD).

## Evolution
### Historical
*   **v1:** Initial design incorporating robot configuration, task run state, logging, and the `on_failure` retry mechanism. 