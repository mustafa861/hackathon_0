---
name: process-whatsapp
description: Process WhatsApp messages and create appropriate responses
---

# Process WhatsApp Skill

This skill processes WhatsApp messages from the Needs_Action folder.

## Usage

When a WhatsApp message file appears in vault/Needs_Action/, this skill:
1. Reads the message content
2. Analyzes urgency and context
3. Creates a draft response
4. Moves to Pending_Approval for human review

## Example

```bash
claude process-whatsapp vault/Needs_Action/WHATSAPP_client_urgent.md
```

## Implementation

The orchestrator automatically triggers this when new WhatsApp files are detected.
