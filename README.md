# Personal AI Employee - Implementation Guide

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ (for MCP servers)
- Claude Code CLI installed
- Obsidian (optional, for GUI)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd hackathon_0
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Playwright (for WhatsApp watcher)**
```bash
playwright install chromium
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Initialize vault structure**
```bash
python scripts/init_vault.py vault/
```

### Configuration

#### 1. Gmail API Setup
1. Go to Google Cloud Console
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download credentials.json to project root

#### 2. WhatsApp Setup (Optional)
1. First run will require manual login
2. Session will be saved for future use
```bash
python src/watchers/whatsapp_watcher.py vault/ .whatsapp_session/
```

#### 3. Claude Code Configuration
Ensure Claude Code is installed and accessible:
```bash
claude --version
```

### Running the System

#### Option 1: Manual Start (Development)
```bash
# Terminal 1: Start orchestrator
python src/orchestrator.py vault/

# Terminal 2: Start Gmail watcher
python src/watchers/gmail_watcher.py vault/ credentials.json

# Terminal 3: Start file system watcher
python src/watchers/filesystem_watcher.py vault/ vault/Drop/
```

#### Option 2: Using Watchdog (Production)
```bash
python src/watchdog.py vault/
```

#### Option 3: Using PM2 (Recommended)
```bash
# Install PM2
npm install -g pm2

# Start all processes
pm2 start ecosystem.config.js

# Save configuration
pm2 save

# Setup startup script
pm2 startup
```

## Project Structure

```
hackathon_0/
├── src/
│   ├── watchers/
│   │   ├── base_watcher.py          # Base class for all watchers
│   │   ├── gmail_watcher.py         # Gmail monitoring
│   │   ├── whatsapp_watcher.py      # WhatsApp monitoring
│   │   └── filesystem_watcher.py    # File drop monitoring
│   ├── utils/
│   │   └── retry_handler.py         # Retry logic with backoff
│   ├── orchestrator.py              # Master process
│   └── watchdog.py                  # Process health monitor
├── vault/                           # Obsidian vault
│   ├── Needs_Action/               # New items to process
│   ├── Pending_Approval/           # Awaiting human approval
│   ├── Approved/                   # Ready to execute
│   ├── Rejected/                   # Rejected actions
│   ├── Done/                       # Completed tasks
│   ├── Plans/                      # AI-generated plans
│   ├── Logs/                       # Audit trail
│   ├── Briefings/                  # Weekly reports
│   ├── Dashboard.md                # Status overview
│   ├── Company_Handbook.md         # Rules and guidelines
│   └── Business_Goals.md           # Objectives and KPIs
├── scripts/
│   └── init_vault.py               # Vault initialization
├── .env.example                    # Environment template
├── requirements.txt                # Python dependencies
├── ecosystem.config.js             # PM2 configuration
├── SPECIFICATIONS.md               # Technical specs
└── README.md                       # This file
```

## Usage

### Processing Tasks

1. **Drop a file** into `vault/Drop/` folder
2. **Send an email** to your monitored Gmail account
3. **Send a WhatsApp message** with keywords (urgent, invoice, etc.)

The system will:
1. Detect the new item
2. Create a file in `Needs_Action/`
3. Claude processes and creates a plan
4. If approval needed, creates file in `Pending_Approval/`
5. You review and move to `Approved/`
6. System executes and logs the action
7. Moves completed task to `Done/`

### Approving Actions

1. Open `vault/Pending_Approval/`
2. Review the action file
3. Move to `Approved/` to proceed
4. Or move to `Rejected/` to cancel

### Monitoring

- **Dashboard**: Open `vault/Dashboard.md` in Obsidian
- **Logs**: Check `vault/Logs/` for daily JSON logs
- **Process status**: `pm2 status` or check watchdog logs

## Implementation Tiers

### Bronze Tier ✅
- [x] Vault structure created
- [x] File system watcher
- [x] Basic orchestrator
- [x] Manual approval workflow
- [x] Logging system

### Silver Tier
- [x] Gmail watcher
- [x] Retry logic
- [x] Watchdog process
- [ ] MCP server integration
- [ ] Scheduled tasks (cron)

### Gold Tier
- [x] WhatsApp watcher
- [ ] Browser automation (Playwright)
- [ ] Weekly CEO briefing
- [ ] Subscription audit
- [ ] Ralph Wiggum loop

### Platinum Tier
- [ ] Cloud deployment
- [ ] Agent-to-Agent communication
- [ ] Offline/online sync
- [ ] Multi-device support

## Security

### Credential Management
- Store API keys in `.env` file (never commit!)
- Use OS keychain for sensitive credentials
- Rotate credentials monthly

### Dry Run Mode
Enable dry run to test without executing real actions:
```bash
export DRY_RUN=true
python src/orchestrator.py vault/
```

### Audit Logs
All actions are logged to `vault/Logs/YYYY-MM-DD.json`:
```json
{
  "timestamp": "2026-03-25T15:39:00Z",
  "action_type": "email_send",
  "target": "client@example.com",
  "approval_status": "approved",
  "result": "success"
}
```

## Troubleshooting

### Watchers not starting
- Check Python version: `python --version` (need 3.10+)
- Verify dependencies: `pip install -r requirements.txt`
- Check logs in `vault/Logs/`

### Gmail API errors
- Verify credentials.json exists
- Check OAuth consent screen is configured
- Ensure Gmail API is enabled in Google Cloud Console

### Claude Code not responding
- Verify installation: `claude --version`
- Check PATH configuration
- Review orchestrator logs

### Process crashes
- Watchdog should auto-restart
- Check `vault/Logs/watchdog.log`
- Review system resources (memory, disk)

## Development

### Adding a New Watcher
1. Inherit from `BaseWatcher`
2. Implement `check_for_updates()` and `create_action_file()`
3. Add to watchdog configuration
4. Test in isolation first

### Adding a New MCP Server
1. Create MCP server following Anthropic specs
2. Add to Claude Code configuration
3. Update orchestrator to invoke
4. Test with dry run mode

### Testing
```bash
# Test individual watcher
python src/watchers/gmail_watcher.py vault/ credentials.json

# Test orchestrator
python src/orchestrator.py vault/

# Test with dry run
export DRY_RUN=true
python src/orchestrator.py vault/
```

## Contributing

This is a hackathon project. Feel free to:
- Add new watchers
- Improve error handling
- Add new MCP integrations
- Enhance the dashboard
- Improve documentation

## License

MIT License - See LICENSE file

## Support

For issues or questions:
- Check troubleshooting section
- Review logs in `vault/Logs/`
- Open an issue on GitHub

## Acknowledgments

- Built for Personal AI Employee Hackathon 0
- Powered by Claude Code (Anthropic)
- Uses Obsidian for knowledge management
- Inspired by the concept of autonomous FTEs

---

**Ready to get started?** Run `python scripts/init_vault.py vault/` to initialize your AI Employee!
