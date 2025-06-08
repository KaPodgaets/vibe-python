---
id: TASK-2025-003
title: "Define Core Data Models"
status: ready
priority: high
type: feature
estimate: 'M'
assignee: '@vibe-team'
created: 2025-06-08
updated: 2025-06-08
parents: [TASK-2025-001]
children: []
arch_refs: [ARCH-data-models]
audit_log:
  - {date: 2025-06-08, user: "@AI-DocArchitect", action: "created with status ready"}
---
## Description
Create the Pydantic and SQLAlchemy models in a central `src/vibe_python/models.py` file. These models will be used for configuration validation and database schema definition.

## Acceptance Criteria
*   A `src/vibe_python/models.py` file is created.
*   Pydantic models for `Robot`, `Action`, `Schedule`, and `OnFailure` are defined.
*   SQLAlchemy models for `TaskRun` and `LogEntry` are defined, including the `retry_count` column on `TaskRun`.

## Definition of Done
*   The `models.py` file is implemented and passes linting. 