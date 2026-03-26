---
name: process-email
description: Process incoming emails from vault and create appropriate responses
---

# Process Email Skill

This skill processes emails from the Needs_Action folder and creates draft responses.

## Usage

When an email file appears in vault/Needs_Action/, this skill:
1. Reads the email content
2. Analyzes the request
3. Creates a draft response
4. Moves to Pending_Approval for human review

## Example

```bash
claude process-email vault/Needs_Action/EMAIL_client_inquiry.md
```

## Implementation

The orchestrator automatically triggers this when new email files are detected.
