# Changelog

All notable changes to the Personal AI Employee project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-25

### Added - Initial Release

#### Core System
- Complete Obsidian vault structure with organized folders
- Base watcher class for extensible monitoring
- Orchestrator for coordinating all system components
- Watchdog process for automatic restart of failed components
- Comprehensive logging system with daily JSON logs

#### Watchers
- Gmail watcher with OAuth authentication
- WhatsApp watcher using Playwright automation
- File system watcher for dropped files
- Configurable check intervals for each watcher

#### MCP Servers
- Email MCP server for sending and drafting emails
- Browser MCP server for web automation
- Support for dry-run mode in all MCP servers

#### Security Features
- Environment-based credential management
- Human-in-the-loop approval workflow
- Comprehensive audit logging
- Rate limiting for actions
- Permission boundaries by action type
- Dry-run mode for safe testing

#### Documentation
- Complete README with setup instructions
- Technical specifications document
- Project summary and architecture overview
- Security policy documentation
- Submission checklist for hackathon
- Contributing guidelines
- Code comments and docstrings

#### Configuration
- Python requirements file
- PM2 ecosystem configuration
- Environment variable templates
- Git ignore rules
- Claude Code MCP configuration
- Startup scripts for Windows and Linux/Mac

#### Testing
- Test suite for core components
- Vault initialization tests
- Watcher functionality tests
- Retry handler tests

#### Templates
- Dashboard template for status monitoring
- Company Handbook for behavior guidelines
- Business Goals for objectives and KPIs
- Folder README files explaining purposes

### Implementation Tiers Achieved
- ✅ Bronze Tier: Basic functionality complete
- ✅ Silver Tier: Multiple watchers and retry logic
- ✅ Gold Tier: WhatsApp, browser automation, MCP servers

### Known Limitations
- WhatsApp watcher requires manual login on first run
- Gmail API requires OAuth setup
- Browser automation limited to Chromium
- No cloud deployment (Platinum tier)
- No agent-to-agent communication yet

### Dependencies
- Python 3.10+
- google-auth-oauthlib 1.2.0
- google-api-python-client 2.116.0
- playwright 1.41.0
- watchdog 3.0.0
- psutil 5.9.8
- requests 2.31.0

### Security Notes
- All credentials stored in environment variables
- Sensitive files excluded from version control
- Approval required for payments > $100
- All actions logged for audit trail
- Dry-run mode enabled by default

---

## Future Roadmap

### [2.0.0] - Platinum Tier (Planned)
- Cloud deployment support
- Agent-to-agent communication
- Offline/online synchronization
- Multi-device support
- Enhanced dashboard with real-time updates

### [1.1.0] - Enhanced Features (Planned)
- Weekly CEO briefing generator
- Subscription audit and cost optimization
- Ralph Wiggum loop implementation
- Custom MCP server templates
- Integration with Odoo ERP
- Slack/Discord notifications

### [1.0.1] - Bug Fixes (Planned)
- Improve error messages
- Better handling of API rate limits
- Enhanced retry logic
- Performance optimizations

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.
