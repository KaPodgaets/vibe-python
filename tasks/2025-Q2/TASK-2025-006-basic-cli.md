---
id: TASK-2025-006
title: "Build a Basic CLI for Manual Triggering"
status: ready
priority: high
type: feature
estimate: 'S'
assignee: '@vibe-team'
created: 2025-06-08
updated: 2025-06-08
parents: [TASK-2025-001]
children: []
arch_refs: [ARCH-cli-orchestrator, ARCH-executor, ARCH-config-manager]
audit_log:
  - {date: 2025-06-08, user: "@AI-DocArchitect", action: "created with status ready"}
---
## Description
Implement the initial command-line interface using `Typer` in `src/vibe_python/main.py`. The primary goal is to create the `run-now` command to test the core executor.

## Acceptance Criteria
*   A `main.py` file is created with a `Typer` application.
*   A `run-now <robot_name>` command is implemented.
*   This command successfully loads a robot definition from a JSON file (hardcoded path for now), and passes it to the `Executor` for execution.
*   A `list-robots` command is also implemented. 