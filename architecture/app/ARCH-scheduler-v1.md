---
id: ARCH-scheduler
title: "Task Scheduler"
type: component
layer: application
owner: @vibe-team
version: v1
status: current
created: 2025-06-08
updated: 2025-06-08
tags: [scheduler, cron, apscheduler]
depends_on: [ARCH-config-manager, ARCH-dal]
referenced_by: []
---
## Context
The Task Scheduler is responsible for automatically queueing robot tasks based on their defined schedules. It ensures that robots are run at their configured times without manual intervention.

## Structure
*   **Primary File:** `src/vibe_python/scheduler.py`
*   **Framework:** `APScheduler`
*   **Key Responsibilities:**
    *   On application startup, it reads all robot configurations via the `Configuration Manager`.
    *   For each `enabled` robot with a `schedule` defined, it adds a job to the `APScheduler` instance.
    *   The scheduled job's only responsibility is to create a new task entry in the `TaskRuns` table with a status of `Pending` by calling a method on the `Data Access Layer (DAL)`.

## Behavior
*   The scheduler is decoupled from the `Executor`. Its role is strictly to add tasks to the queue at the correct time. The main orchestration loop is responsible for picking up these queued tasks and passing them to the `Executor`.
*   This design prevents a long-running robot from blocking the scheduling of other robots.

## Evolution
### Historical
*   **v1:** Initial design using `APScheduler` to create database entries for pending tasks. 