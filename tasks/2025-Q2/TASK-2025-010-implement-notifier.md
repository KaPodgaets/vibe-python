---
id: TASK-2025-010
title: "Implement Email Notifier"
status: backlog
priority: high
type: feature
estimate: 'M'
assignee: '@vibe-team'
created: 2025-06-08
updated: 2025-08-08
parents: [TASK-2025-007]
children: []
arch_refs: [ARCH-notifier]
audit_log:
  - {date: 2025-06-08, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Create the email notification component in `src/vibe_python/notifier.py`. This module will be responsible for sending email alerts for terminally failed tasks.

## Acceptance Criteria
*   The `notifier.py` module is created.
*   It contains a function that can send an email using SMTP credentials from the `.env` file.
*   The email body is templated and contains relevant failure information (robot name, timestamp, error). 