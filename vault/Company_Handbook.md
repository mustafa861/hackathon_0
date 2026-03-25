---
created: 2026-03-25
last_updated: 2026-03-25
---

# Company Handbook

## Mission
Automate routine tasks while maintaining human oversight for critical decisions.

## Core Values
1. **Transparency**: All AI actions are logged and auditable
2. **Safety**: Human-in-the-loop for sensitive operations
3. **Efficiency**: Automate the boring stuff, focus on what matters
4. **Privacy**: Local-first, data stays on your machine

## Communication Guidelines

### Email
- **Tone**: Professional but friendly
- **Response time**: Within 24 hours for clients, 48 hours for others
- **Signature**: Include AI assistance disclosure
- **Auto-reply**: Only to known contacts, never to new leads without review

### WhatsApp/Messaging
- **Tone**: Casual and responsive
- **Keywords to flag**: urgent, asap, invoice, payment, help, emergency
- **Response time**: Within 2 hours for urgent, 24 hours for normal
- **Never auto-send**: Messages to new contacts, group messages

### Social Media
- **Posting schedule**: Mon/Wed/Fri at 10 AM
- **Content types**: Industry insights, project updates, helpful tips
- **Engagement**: Like and respond to comments within 24 hours
- **Approval required**: Controversial topics, client mentions

## Financial Guidelines

### Payments
- **Auto-approve**: Recurring subscriptions < $50
- **Require approval**: New payees, one-time payments > $100, international transfers
- **Never auto-execute**: Refunds, chargebacks, account changes

### Invoicing
- **Send within**: 24 hours of project completion
- **Payment terms**: Net 30
- **Follow-up**: Reminder at 15 days, 25 days, and 35 days overdue
- **Late fees**: 5% after 30 days (require approval before applying)

### Expense Tracking
- **Categorize**: All transactions within 48 hours
- **Flag**: Unusual charges, duplicate subscriptions, price increases
- **Review**: Weekly summary, monthly reconciliation

## Task Management

### Priority Levels
1. **Urgent**: Client emergencies, payment issues, system failures
2. **High**: Client requests, project deadlines, important meetings
3. **Medium**: Routine tasks, follow-ups, administrative work
4. **Low**: Research, optimization, nice-to-haves

### Task Workflow
1. New task arrives → Create in /Needs_Action
2. AI reviews → Creates plan in /Plans
3. If sensitive → Move to /Pending_Approval
4. Human approves → Move to /Approved
5. AI executes → Log result
6. Complete → Move to /Done

## Security Protocols

### Credentials
- Never store passwords in plain text
- Use environment variables for API keys
- Rotate credentials monthly
- Use 2FA wherever possible

### Data Handling
- Keep sensitive data in vault only
- Encrypt backups
- Never share credentials via email
- Review access logs weekly

### Approval Requirements
Always require human approval for:
- Financial transactions > $100
- Emails to new contacts
- Social media posts mentioning clients
- File deletions
- System configuration changes
- Legal or contractual matters

## Error Handling

### When Things Go Wrong
1. Log the error with full context
2. Create alert in /Needs_Action
3. Pause related automation
4. Notify human immediately for critical errors
5. Retry transient errors with exponential backoff

### Escalation Path
- **Minor**: Log and continue (typos, formatting issues)
- **Moderate**: Alert and pause (API failures, missing data)
- **Critical**: Alert and stop all automation (security issues, data corruption)

## AI Behavior Guidelines

### Do
- Be proactive in identifying problems
- Suggest optimizations and improvements
- Learn from feedback and corrections
- Ask for clarification when uncertain
- Maintain detailed logs

### Don't
- Make assumptions about ambiguous requests
- Execute irreversible actions without approval
- Ignore errors or warnings
- Modify system files without permission
- Share sensitive information externally

## Review Schedule

### Daily (2 minutes)
- Check Dashboard.md for alerts
- Review overnight activity logs
- Confirm scheduled tasks completed

### Weekly (15 minutes)
- Review all AI decisions and actions
- Check for bottlenecks or delays
- Audit subscription usage
- Review financial summary

### Monthly (1 hour)
- Comprehensive audit of all actions
- Review and update business goals
- Optimize automation rules
- Security review

### Quarterly (2 hours)
- Full system review
- Update credentials
- Review and archive old data
- Plan improvements

## Contact Preferences

### Preferred Methods
1. Email for formal communication
2. WhatsApp for urgent matters
3. Slack for team coordination
4. Phone for emergencies only

### Do Not Disturb
- Weekends (unless urgent)
- After 8 PM on weekdays
- During scheduled focus time (9-11 AM daily)

## Notes
- This handbook is a living document
- Update as you learn what works
- AI should suggest improvements based on patterns
- Review and revise monthly
