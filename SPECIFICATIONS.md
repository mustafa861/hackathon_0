# Personal AI Employee - Technical Specifications

## Project Overview
Build an autonomous AI Employee system that manages personal and business affairs 24/7 using Claude Code as the reasoning engine and Obsidian as the management dashboard.

## System Architecture

### Core Components

#### 1. Perception Layer (Watchers)
- **Gmail Watcher**: Monitors inbox for important/unread emails
- **WhatsApp Watcher**: Tracks urgent messages via Playwright automation
- **Finance Watcher**: Monitors bank transactions and downloads CSVs
- **File System Watcher**: Detects dropped files for processing

#### 2. Memory Layer (Obsidian Vault)
```
/Vault/
├── Needs_Action/          # New items requiring processing
├── Pending_Approval/      # Actions awaiting human approval
├── Approved/              # Human-approved actions ready to execute
├── Rejected/              # Rejected actions
├── Done/                  # Completed tasks
├── Plans/                 # AI-generated action plans
├── Logs/                  # Audit trail (JSON format)
├── Briefings/             # Weekly CEO briefings
├── Dashboard.md           # Real-time status summary
├── Company_Handbook.md    # Rules and guidelines
├── Business_Goals.md      # Objectives and KPIs
└── Accounting/            # Financial records
```

#### 3. Reasoning Layer (Claude Code)
- Reads from Needs_Action folder
- Creates plans with checkboxes
- Writes approval requests for sensitive actions
- Uses Ralph Wiggum loop for task persistence

#### 4. Action Layer (MCP Servers)
- **Email MCP**: Send/draft/search emails
- **Browser MCP**: Navigate websites, fill forms, make payments
- **Calendar MCP**: Schedule events
- **Slack MCP**: Team communication

#### 5. Orchestration Layer
- **Orchestrator.py**: Master process managing timing and folder watching
- **Watchdog.py**: Health monitor that restarts failed processes

## Implementation Tiers

### Bronze Tier (Minimum Viable)
- Obsidian vault with folder structure
- One watcher (Gmail or file system)
- Claude Code reads and writes to vault
- Manual approval workflow (move files between folders)
- Basic logging

### Silver Tier (Recommended)
- All Bronze features
- 2+ watchers running
- MCP server integration (email)
- Ralph Wiggum loop for persistence
- Automated scheduling (cron/Task Scheduler)
- Retry logic with exponential backoff

### Gold Tier (Advanced)
- All Silver features
- 3+ watchers including WhatsApp
- Browser automation for payments
- Weekly CEO briefing generation
- Subscription audit and cost optimization
- Comprehensive error handling and recovery

### Platinum Tier (Cloud Integration)
- All Gold features
- Cloud-based Claude instance for 24/7 operation
- Agent-to-Agent (A2A) communication
- Offline/online synchronization
- Multi-device support

## Security Requirements

### Credential Management
- Use environment variables for API keys
- Store sensitive credentials in OS keychain
- Create .env file (add to .gitignore)
- Rotate credentials monthly

### Sandboxing
- DEV_MODE flag to prevent real actions during development
- --dry-run support in all action scripts
- Separate test accounts for development
- Rate limiting (max 10 emails/hour, max 3 payments/hour)

### Audit Logging
Required log format:
```json
{
  "timestamp": "2026-03-25T15:30:00Z",
  "action_type": "email_send",
  "actor": "claude_code",
  "target": "client@example.com",
  "parameters": {"subject": "Invoice #123"},
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

### Permission Boundaries
| Action Category | Auto-Approve | Always Require Approval |
|-----------------|--------------|-------------------------|
| Email replies | Known contacts | New contacts, bulk sends |
| Payments | < $50 recurring | All new payees, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move outside vault |

## Error Handling

### Error Categories
- **Transient**: Network timeout, API rate limit → Exponential backoff retry
- **Authentication**: Expired token → Alert human, pause operations
- **Logic**: Misinterpretation → Human review queue
- **Data**: Corrupted file → Quarantine + alert
- **System**: Process crash → Watchdog auto-restart

### Retry Logic
- Max 3 attempts
- Exponential backoff: 1s, 2s, 4s
- Max delay: 60s
- Never retry payments automatically

### Graceful Degradation
- Gmail API down → Queue emails locally
- Banking API timeout → Require fresh approval
- Claude Code unavailable → Queue tasks
- Obsidian vault locked → Write to temp folder

## Key Features

### Monday Morning CEO Briefing
Generated every Sunday night, includes:
- Revenue summary (week, MTD, trend)
- Completed tasks
- Bottlenecks (tasks with delays)
- Proactive suggestions (cost optimization, upcoming deadlines)

### Human-in-the-Loop (HITL)
For sensitive actions:
1. Claude creates approval request file in /Pending_Approval
2. Human reviews and moves to /Approved or /Rejected
3. Orchestrator detects approval and executes via MCP
4. Result logged to /Logs

### Ralph Wiggum Loop
Keeps Claude working until task completion:
1. Orchestrator creates state file with prompt
2. Claude processes task
3. Stop hook checks if task file moved to /Done
4. If not done, re-inject prompt and continue
5. Repeat until complete or max iterations (10)

## Tech Stack

- **Knowledge Base**: Obsidian (Local Markdown)
- **Logic Engine**: Claude Code (Opus 4.6)
- **Watchers**: Python 3.10+
- **Browser Automation**: Playwright
- **Process Management**: PM2 or supervisord
- **MCP Servers**: Node.js/Python
- **Scheduling**: cron (Mac/Linux) or Task Scheduler (Windows)

## Dependencies

### Python Packages
```
google-auth-oauthlib
google-api-python-client
playwright
watchdog
python-dotenv
requests
```

### Node.js Packages
```
pm2 (global)
@anthropic/browser-mcp
```

## Judging Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Functionality | 30% | Does it work? Core features complete? |
| Innovation | 25% | Creative solutions, novel integrations |
| Practicality | 20% | Would you use this daily? |
| Security | 15% | Proper credential handling, HITL safeguards |
| Documentation | 10% | Clear README, setup instructions, demo |

## Submission Requirements

1. GitHub repository (public or private with judge access)
2. README.md with setup instructions and architecture overview
3. Demo video (5-10 minutes) showing key features
4. Security disclosure: How credentials are handled
5. Tier declaration: Bronze, Silver, Gold, or Platinum
6. Submit form: https://forms.gle/JR9T1SJq5rmQyGkGA

## Success Metrics

- **Autonomy**: % of tasks completed without human intervention
- **Accuracy**: % of AI decisions that were correct
- **Response Time**: Average time from trigger to action
- **Cost Savings**: Hours saved per week
- **Reliability**: Uptime % of watcher processes

## Ethical Guidelines

### When AI Should NOT Act Autonomously
- Emotional contexts (condolences, conflict resolution)
- Legal matters (contracts, regulatory filings)
- Medical decisions
- Financial edge cases (unusual transactions, new recipients)
- Irreversible actions

### Transparency Principles
- Disclose AI involvement in communications
- Maintain audit trails
- Allow opt-out for contacts
- Schedule weekly reviews of AI decisions

### Privacy Considerations
- Minimize data collection
- Local-first architecture
- Encrypt vault at rest
- Understand third-party API data sharing

## Oversight Schedule

- **Daily**: 2-minute dashboard check
- **Weekly**: 15-minute action log review
- **Monthly**: 1-hour comprehensive audit
- **Quarterly**: Full security and access review
