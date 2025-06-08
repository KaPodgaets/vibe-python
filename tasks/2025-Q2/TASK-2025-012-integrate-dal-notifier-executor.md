---
id: TASK-2025-012
title: "Integrate DAL and Notifier with the Executor"
status: backlog
priority: high
type: feature
estimate: 'M'
assignee: '@vibe-team'
created: 2025-06-08
updated: 2025-06-08
parents: [TASK-2025-007]
children: []
arch_refs: [ARCH-executor, ARCH-dal, ARCH-notifier]
audit_log:
  - {date: 2025-06-08, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Connect the `Executor` to the `DAL` and `Notifier` to complete the full, resilient task execution lifecycle.

## Acceptance Criteria
*   The `Executor` calls the `DAL` to create/update `TaskRun` records (e.g., set status to 'Running', increment `retry_count`).
*   The `Executor` calls the `DAL` to write to the `LogEntries` table.
*   Upon final failure of a task, the `Executor` calls the `Notifier` to send an email alert before setting the task status to 'Failed'.
*   On failure, a screenshot of the desktop is captured and its path is logged to the database. 