---
id: TASK-2025-020
title: "Document Application Execution"
status: done
priority: medium
type: chore
estimate: 'S'
assignee: '@AI-DocArchitect'
created: 2025-06-08
updated: 2025-06-08
parents: []
children: []
arch_refs: [ARCH-cli-orchestrator]
audit_log:
  - {date: 2025-06-08, user: "@AI-DocArchitect", action: "created with status done"}
---
## Description
A bug report (`bugs/001.md`) revealed that running the application via `python src/vibe_python/main.py` causes an `ImportError`. This is because the application is designed as an installable package and must be run as such. This task is to create documentation outlining the correct way to install and run the application to prevent this issue.

## Acceptance Criteria
*   A new architecture document, `ARCH-execution-guide`, is created.
*   The guide clearly explains why direct script execution fails.
*   The guide provides step-by-step instructions for the two correct execution methods:
    1. Installing the package in editable mode (`pip install -e .`) and using the console script (`vibe-python`).
    2. Running the package as a module (`python -m vibe_python.main`).

## Definition of Done
*   The `ARCH-execution-guide-v1.md` file is created and contains the necessary instructions. 