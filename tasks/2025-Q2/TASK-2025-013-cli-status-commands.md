---
id: TASK-2025-013
title: "Implement CLI Status Commands"
status: backlog
priority: high
type: feature
estimate: 'S'
assignee: '@vibe-team'
created: 2025-06-08
updated: 2025-06-08
parents: [TASK-2025-007]
children: []
arch_refs: [ARCH-cli-orchestrator, ARCH-dal]
audit_log:
  - {date: 2025-06-08, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Enhance the CLI with commands that allow the user to query the state of the system from the database.

## Acceptance Criteria
*   A `vibe-python status [--limit N]` command is implemented that shows the status of the last N task runs.
*   A `vibe-python status <task_run_id>` command shows detailed status and logs for a specific run.
*   A `vibe-python rerun <task_run_id>` command is implemented to re-queue a past task. 