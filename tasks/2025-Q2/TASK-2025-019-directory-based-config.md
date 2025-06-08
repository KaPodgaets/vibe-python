---
id: TASK-2025-019
title: "Refactor Configuration Manager for Directory Loading"
status: backlog
priority: low
type: feature
estimate: 'M'
assignee: '@vibe-team'
created: 2025-06-08
updated: 2025-06-08
parents: [TASK-2025-018]
children: []
arch_refs: [ARCH-config-manager, ARCH-cli-orchestrator]
audit_log:
  - {date: 2025-06-08, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Refactor the `Configuration Manager` to support loading all `*.json` files from the `configs/robots.d/` directory, instead of a single file.

## Acceptance Criteria
*   The `config.py` module is updated to scan, load, and consolidate all robot configurations from the directory.
*   The system raises a startup error if duplicate `robot_name` values are detected.
*   All CLI commands that rely on robot configurations (e.g., `list-robots`, `run-now`) work correctly with the consolidated list. 