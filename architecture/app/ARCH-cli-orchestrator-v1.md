---
id: ARCH-cli-orchestrator
title: "CLI and Orchestrator"
type: component
layer: presentation
owner: @vibe-team
version: v1
status: current
created: 2025-06-08
updated: 2025-06-08
tags: [cli, orchestrator, service]
depends_on: [ARCH-scheduler, ARCH-executor, ARCH-dal, ARCH-config-manager]
referenced_by: []
---
## Context
This component serves as the main entry point and user interface for the RPA orchestration application. It provides a Command Line Interface (CLI) for manual control, status checks, and service management. It also contains the main orchestration loop that drives the entire application when running as a service.

## Structure
*   **Primary File:** `src/vibe_python/main.py`
*   **Framework:** `Typer` is used for building the CLI.
*   **Key Responsibilities:**
    *   Initializing all other core components (Configuration Manager, DAL, Executor, Scheduler).
    *   Defining CLI commands such as `start-service`, `restart-service`, `run-now`, `status`, `list-robots`, and `rerun`.
    *   For the `start-service` command, it initiates the scheduler and then enters a persistent worker loop that calls the Executor to process tasks from the database queue.
    *   Manages the process ID (`.pid`) file for service control.

## Behavior
*   **User Interaction:** Users interact with the system primarily through the commands defined in this component. For example, `vibe-python run-now <robot_name>` will trigger an immediate task run.
*   **Service Orchestration:** The `start-service` command runs a loop that:
    1.  Starts the `Scheduler` to queue jobs based on their cron schedules.
    2.  Continuously polls the database (via the `DAL`) for `Pending` tasks.
    3.  Passes any found tasks to the `Executor` for processing.
*   **Dependencies:** It coordinates all other major components, acting as the central nervous system of the application. It relies on the `Configuration Manager` to know which robots exist, the `DAL` to interact with the task queue, the `Scheduler` to manage time-based jobs, and the `Executor` to run the robots.

## Evolution
### Planned
*   No major changes are planned for the core orchestration logic, but new CLI commands may be added as features are developed.

### Historical
*   **v1:** Initial design based on the greenfield project plan. Defines core service management and user-facing commands. 