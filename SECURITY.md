# Security Policy

## Credential Management

### Environment Variables
All sensitive credentials are stored in environment variables via the `.env` file:

```bash
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
BANK_API_TOKEN=your_token
```

**Important:**
- `.env` file is excluded from version control via `.gitignore`
- Never commit credentials to the repository
- Use `.env.example` as a template
- Rotate credentials monthly

### OAuth Tokens
- Gmail OAuth tokens are stored in `.gmail_token.pickle`
- This file is also excluded from version control
- Tokens are refreshed automatically when expired
- Stored in the vault directory (not in the repository)

### WhatsApp Session
- WhatsApp session data stored in `.whatsapp_session/` directory
- Excluded from version control
- Contains browser session cookies
- Should be treated as sensitive

## Human-in-the-Loop (HITL) Approval Workflow

### Approval Required For
The system requires explicit human approval for:

1. **Financial Actions**
   - Payments over $100
   - Payments to new recipients
   - Any international transfers
   - Refunds or chargebacks

2. **Communication**
   - Emails to new contacts
   - Bulk email sends
   - Social media posts mentioning clients
   - Direct messages on any platform

3. **Destructive Actions**
   - File deletions
   - Moving files outside vault
   - System configuration changes
   - Account modifications

### Approval Process
1. AI creates action file in `vault/Pending_Approval/`
2. Human reviews the action details
3. Human moves file to `vault/Approved/` to proceed
4. Or moves to `vault/Rejected/` to cancel
5. Orchestrator executes only approved actions
6. Result is logged to `vault/Logs/`

## Audit Logging

### What is Logged
Every AI action is logged with:
- Timestamp (ISO 8601 format)
- Action type (email_send, payment, file_operation, etc.)
- Actor (always "claude_code")
- Target (recipient, file path, etc.)
- Parameters (subject, amount, etc.)
- Approval status (approved/rejected/auto)
- Approved by (human/auto)
- Result (success/error)

### Log Format
```json
{
  "timestamp": "2026-03-25T15:44:00Z",
  "action_type": "email_send",
  "actor": "claude_code",
  "target": "client@example.com",
  "parameters": {"subject": "Invoice #123"},
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

### Log Storage
- Daily JSON files: `vault/Logs/YYYY-MM-DD.json`
- Watcher logs: `vault/Logs/<watcher_name>.log`
- Retention: Minimum 90 days
- Review: Weekly for anomalies

## Dry-Run Mode

### Purpose
Dry-run mode allows testing the system without executing real actions.

### Enabling Dry-Run
Set in `.env` file:
```bash
DRY_RUN=true
```

### Behavior in Dry-Run
- All actions are logged but not executed
- Email sends are simulated
- Payments are not processed
- Browser automation stops before submission
- Logs show `[DRY RUN]` prefix

### Recommended Usage
- Always use dry-run for initial testing
- Test with dry-run after configuration changes
- Disable only when confident in setup

## Rate Limiting

### Configured Limits
- Maximum 10 emails per hour
- Maximum 3 payments per hour
- Configurable in `.env` file

### Purpose
- Prevent accidental bulk operations
- Protect against runaway automation
- Comply with API rate limits

### Enforcement
- Tracked in orchestrator
- Exceeded limits trigger alerts
- Actions queued until limit resets

## Permission Boundaries

### Auto-Approve Thresholds
| Action Category | Auto-Approve | Require Approval |
|-----------------|--------------|------------------|
| Email replies | Known contacts | New contacts, bulk |
| Payments | < $50 recurring | New payees, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move outside vault |

### Customization
Edit `vault/Company_Handbook.md` to adjust thresholds for your needs.

## Data Privacy

### Local-First Architecture
- All data stored locally in Obsidian vault
- No cloud storage by default
- Sensitive data never leaves your machine
- You control all data

### Third-Party APIs
Data shared with external services:
- **Gmail API**: Email metadata and content (Google's privacy policy applies)
- **WhatsApp Web**: Message content (WhatsApp's terms apply)
- **Banking APIs**: Transaction data (Bank's privacy policy applies)

### Encryption
- Consider encrypting your Obsidian vault at rest
- Use full-disk encryption on your machine
- Secure backup storage

## Incident Response

### If Credentials are Compromised
1. Immediately revoke all API tokens
2. Change all passwords
3. Review audit logs for unauthorized actions
4. Rotate all credentials
5. Update `.env` file

### If Unauthorized Action Occurs
1. Stop all processes immediately
2. Review `vault/Logs/` for the action
3. Identify root cause
4. Implement additional safeguards
5. Update `vault/Company_Handbook.md` rules

### Reporting Security Issues
If you discover a security vulnerability:
1. Do NOT open a public GitHub issue
2. Email security concerns to: [your-email]
3. Include detailed description and reproduction steps
4. Allow time for fix before public disclosure

## Best Practices

### For Users
1. Review dashboard daily (2 minutes)
2. Audit logs weekly (15 minutes)
3. Rotate credentials monthly
4. Keep software updated
5. Use strong, unique passwords
6. Enable 2FA on all accounts

### For Developers
1. Never commit credentials
2. Use environment variables
3. Implement approval gates for sensitive actions
4. Log all actions comprehensively
5. Test with dry-run mode first
6. Follow principle of least privilege

## Compliance

### GDPR Considerations
- Data stored locally (data controller is the user)
- No data shared with third parties except via APIs
- User has full control over data deletion
- Audit logs provide transparency

### Financial Regulations
- Payment actions require explicit approval
- All transactions logged
- No automated trading or investment decisions
- User remains responsible for all financial actions

## Updates

This security policy will be updated as:
- New features are added
- Security best practices evolve
- Vulnerabilities are discovered
- User feedback is received

Last updated: 2026-03-25

---

**Remember:** You are responsible for all actions taken by your AI Employee. Regular oversight is essential, not optional.
