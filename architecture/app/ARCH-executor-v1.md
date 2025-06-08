---
id: ARCH-executor
title: "Executor / Robot Engine"
type: component
layer: application
owner: @vibe-team
version: v1
status: current
created: 2025-06-08
updated: 2025-06-08
tags: [worker, rpa, pyautogui, retry]
depends_on: [ARCH-config-manager, ARCH-dal, ARCH-notifier]
referenced_by: []
---
## Context
The Executor is the core worker component of the application. It is responsible for picking up a pending task from the queue and executing the sequence of RPA actions defined in the corresponding robot's configuration.

## Structure
*   **Primary File:** `src/vibe_python/executor.py`
*   **Key RPA Library:** `pyautogui`
*   **Key Responsibilities:**
    *   Processes one task at a time in a single-threaded manner to avoid conflicts with GUI interactions.
    *   Translates the declarative list of actions (e.g., `{"type": "click", ...}`) into imperative calls to the `pyautogui` library.
    *   Manages the lifecycle of a task run, updating its status in the database from `Pending` to `Running`, and finally to `Success` or `Failed`.
    *   Implements a session keep-alive mechanism (e.g., a periodic, non-disruptive mouse move) to prevent the RDP session from locking during long periods of inactivity between tasks.

## Behavior
*   **Task Execution:** The main orchestrator loop passes a `TaskRun` object to the executor.
*   **Retry Logic:** The executor reads the `on_failure` policy from the robot's configuration. It wraps the entire action sequence execution in a retry loop.
    1.  If an action fails, the attempt is logged, the `retry_count` in the database is incremented (via the `DAL`), and the executor waits for the specified `delay_seconds`.
    2.  This repeats until the task succeeds or the number of retries is exhausted.
*   **Failure Handling:** If a task fails on its final attempt, the executor:
    1.  Takes a screenshot of the desktop for debugging.
    2.  Logs a detailed error message to the database.
    3.  Calls the `Notifier` to send an email alert.
    4.  Sets the task's final status to `Failed`.

## Evolution
### Planned
*   The action execution logic could be refactored to use a Strategy Pattern to allow for different RPA backends in the future (e.g., Selenium for web automation).

### Historical
*   **v1:** Initial design. Includes core action execution, robust retry/failure logic, and session keep-alive. 