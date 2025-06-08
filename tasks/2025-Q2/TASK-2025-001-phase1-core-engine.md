---
id: TASK-2025-001
title: "Phase 1: Core Engine & Manual Execution"
status: ready
priority: high
type: feature
estimate: 'L'
assignee: '@vibe-team'
created: 2025-06-08
updated: 2025-06-08
parents: []
children: [TASK-2025-002, TASK-2025-003, TASK-2025-004, TASK-2025-005, TASK-2025-006]
arch_refs: [ARCH-cli-orchestrator, ARCH-executor, ARCH-data-models]
risk: medium
audit_log:
  - {date: 2025-06-08, user: "@AI-DocArchitect", action: "created with status ready"}
---
## Description
This epic covers the foundational work to build the core components of the RPA orchestrator. The goal is to have a system where a developer can manually trigger a defined robot from the command line and have it execute its actions. This phase focuses on the core execution logic, configuration, and session stability, without database persistence or automated scheduling.

## Acceptance Criteria
*   The project structure is established according to the design plan.
*   Robot actions can be defined in a JSON file and parsed by the application.
*   A CLI command exists to manually run a specific robot by name (`vibe-python run-now <robot_name>`).
*   The application can prevent the RDP session from locking while a robot is active.

## Definition of Done
*   All child tasks (TASK-2025-002 to TASK-2025-006) are completed and marked as 'done'.
*   The core engine can be demonstrated by running a simple robot manually from the CLI. 