---
name: process-social-media
description: Process social media messages from LinkedIn, Facebook, Instagram, Twitter
---

# Process Social Media Skill

This skill processes social media messages and interactions.

## Usage

When a social media file appears in vault/Needs_Action/, this skill:
1. Reads the message/mention content
2. Analyzes context and intent
3. Creates appropriate response
4. Moves to Pending_Approval for human review

## Supported Platforms

- LinkedIn messages and connection requests
- Facebook messages
- Instagram DMs
- Twitter/X mentions and DMs

## Example

```bash
claude process-social-media vault/Needs_Action/LINKEDIN_message_*.md
```

## Implementation

The orchestrator automatically triggers this when new social media files are detected.
