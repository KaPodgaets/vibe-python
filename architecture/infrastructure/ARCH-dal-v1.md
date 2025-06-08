---
id: ARCH-dal
title: "Data Access Layer (DAL)"
type: component
layer: infrastructure
owner: @vibe-team
version: v1
status: current
created: 2025-06-08
updated: 2025-06-08
tags: [database, sql, sqlalchemy]
depends_on: [ARCH-data-models]
referenced_by: []
---
## Context
The Data Access Layer (DAL) provides a dedicated abstraction layer for all database interactions. It centralizes database logic, making the application easier to maintain and test, and decouples the core application logic from the specific database implementation (MS SQL Server).

## Structure
*   **Primary File:** `src/vibe_python/database.py`
*   **Framework:** `SQLAlchemy` (Core or ORM)
*   **Key Responsibilities:**
    *   Managing the database connection and session.
    *   Providing high-level functions for Create, Read, Update, and Delete (CRUD) operations on the database tables (`TaskRuns`, `LogEntries`).
    *   Examples of functions: `create_task_run()`, `get_next_pending_task()`, `update_task_status()`, `add_log_entry()`.
    *   Translating between application-level objects and database records, using the models defined in `ARCH-data-models`.

## Behavior
*   All other components that need to interact with the database (e.g., `Scheduler`, `Executor`, `CLI`) must do so exclusively through the functions provided by the DAL. They are never to interact with `SQLAlchemy` or the database driver directly.

## Evolution
### Historical
*   **v1:** Initial design. Provides all necessary CRUD operations for task and log management. 