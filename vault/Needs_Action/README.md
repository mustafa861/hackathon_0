# Needs Action

This folder contains new items that require processing by the AI Employee.

## How it works
1. Watchers detect new emails, messages, or files
2. They create markdown files here with the details
3. Orchestrator triggers Claude Code to process them
4. Claude creates plans and moves items forward

## File naming convention
- EMAIL_<message_id>.md - Email messages
- WHATSAPP_<contact>_<timestamp>.md - WhatsApp messages
- FILE_<filename>.md - Dropped files
- ALERT_<timestamp>.md - System alerts