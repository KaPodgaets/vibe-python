---
id: ARCH-notifier
title: "Email Notifier"
type: component
layer: infrastructure
owner: @vibe-team
version: v1
status: current
created: 2025-06-08
updated: 2025-06-08
tags: [notification, email, smtp]
depends_on: [ARCH-config-manager]
referenced_by: []
---
## Context
The Notifier component is responsible for sending out-of-band notifications, specifically email alerts when a robot task fails permanently (i.e., after all retries are exhausted).

## Structure
*   **Primary File:** `src/vibe_python/notifier.py`
*   **Key Responsibilities:**
    *   Provides a simple function, e.g., `send_failure_notification(task_run_details)`.
    *   Reads email server configuration (SMTP host, port, credentials) and recipient list from the `.env` file via the `Configuration Manager`.
    *   Formats a clear and informative email body, including details like the robot name, time of failure, and the final error message.
    *   Handles potential exceptions during the email sending process to prevent a notification failure from crashing the executor.

## Behavior
*   The `Executor` calls this component only after a task has failed its final retry attempt.

## Evolution
### Historical
*   **v1:** Initial design to support email notifications for failed tasks. 