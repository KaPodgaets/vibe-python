---
id: TASK-2025-016
title: "Create the Main Orchestration Service"
status: backlog
priority: medium
type: feature
estimate: 'M'
assignee: '@vibe-team'
created: 2025-06-08
updated: 2025-06-08
parents: [TASK-2025-014]
children: []
arch_refs: [ARCH-cli-orchestrator, ARCH-scheduler, ARCH-executor]
audit_log:
  - {date: 2025-06-08, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Implement the `start-service` CLI command. This command will start the application as a long-running process, activating both the scheduler and the executor worker loop.

## Acceptance Criteria
*   A `vibe-python start-service` command is created.
*   When run, it starts the `APScheduler` to begin queueing jobs.
*   It then enters a loop that periodically polls the database for 'Pending' tasks and passes them to the `Executor`. 