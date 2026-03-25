# Personal AI Employee - Visual Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL WORLD                                  │
│  📧 Gmail    💬 WhatsApp    🏦 Banking    📁 File Drops                │
└────────┬──────────┬──────────────┬──────────────┬────────────────────────┘
         │          │              │              │
         │          │              │              │ [Continuous Monitoring]
         ▼          ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      PERCEPTION LAYER                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │Gmail Watcher │  │WhatsApp Watch│  │  File Watch  │                 │
│  │  (OAuth)     │  │ (Playwright) │  │  (Watchdog)  │                 │
│  │Every 2 min   │  │Every 30 sec  │  │  Real-time   │                 │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
└─────────┼──────────────────┼──────────────────┼──────────────────────────┘
          │                  │                  │
          │ Creates .md file │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT (Local Storage)                       │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  📥 Needs_Action/                                                 │ │
│  │     EMAIL_abc123.md                                               │ │
│  │     WHATSAPP_client_20260325.md                                   │ │
│  │     FILE_invoice.pdf.md                                           │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  📊 Dashboard.md  │  📖 Company_Handbook.md  │  🎯 Business_Goals │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ Orchestrator detects new files
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      REASONING LAYER                                    │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                      CLAUDE CODE (Opus 4.6)                       │ │
│  │                                                                   │ │
│  │  1. Read files from Needs_Action/                                │ │
│  │  2. Analyze content and context                                  │ │
│  │  3. Check Company_Handbook.md for rules                          │ │
│  │  4. Create action plan in Plans/                                 │ │
│  │  5. Determine if approval needed                                 │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
         [Safe Action]                [Sensitive Action]
                    │                         │
                    ▼                         ▼
         ┌──────────────────┐    ┌──────────────────────────┐
         │  Auto-Execute    │    │  ⚠️  Pending_Approval/   │
         │  - Read files    │    │  - Payments > $100       │
         │  - Create drafts │    │  - New contacts          │
         │  - Log actions   │    │  - Irreversible actions  │
         └────────┬─────────┘    └────────┬─────────────────┘
                  │                       │
                  │                       │ Human reviews
                  │                       ▼
                  │              ┌──────────────────┐
                  │              │  👤 HUMAN        │
                  │              │  Review & Decide │
                  │              └────┬────────┬────┘
                  │                   │        │
                  │              [Approve] [Reject]
                  │                   │        │
                  │                   ▼        ▼
                  │            Approved/   Rejected/
                  │                   │
                  └───────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        ACTION LAYER (MCP Servers)                       │
│  ┌──────────────────────┐         ┌──────────────────────┐            │
│  │   📧 Email MCP       │         │   🌐 Browser MCP     │            │
│  │   - Send email       │         │   - Navigate web     │            │
│  │   - Draft email      │         │   - Fill forms       │            │
│  │   - Search inbox     │         │   - Take screenshots │            │
│  └──────────┬───────────┘         └──────────┬───────────┘            │
└─────────────┼──────────────────────────────────┼──────────────────────────┘
              │                                  │
              │ [Execute Action]                 │
              ▼                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL ACTIONS                                   │
│  ✉️  Send Email    💰 Make Payment    📱 Send Message    📄 Process File│
└─────────────────────────────────────────────────────────────────────────┘
              │
              │ [Log Result]
              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      AUDIT & COMPLETION                                 │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  📝 Logs/2026-03-25.json                                          │ │
│  │  {                                                                │ │
│  │    "timestamp": "2026-03-25T15:48:00Z",                          │ │
│  │    "action_type": "email_send",                                  │ │
│  │    "target": "client@example.com",                               │ │
│  │    "approval_status": "approved",                                │ │
│  │    "result": "success"                                           │ │
│  │  }                                                                │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ✅ Move completed task to Done/                                       │
│  📊 Update Dashboard.md                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Example: Email Processing

```
Step 1: Detection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 New email arrives: "Can you send me the invoice?"
   ↓
Gmail Watcher detects (every 2 minutes)
   ↓
Creates: vault/Needs_Action/EMAIL_abc123.md
---
type: email
from: client@example.com
subject: Invoice Request
priority: high
---


Step 2: Reasoning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Orchestrator detects new file
   ↓
Triggers Claude Code
   ↓
Claude reads:
  - EMAIL_abc123.md
  - Company_Handbook.md (rules)
  - Business_Goals.md (context)
   ↓
Creates: vault/Plans/PLAN_invoice_client.md
---
Objective: Send invoice to client@example.com
Steps:
  [x] Identify client
  [x] Calculate amount: $1,500
  [ ] Generate invoice PDF
  [ ] Send via email (REQUIRES APPROVAL)
---


Step 3: Approval
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Claude creates: vault/Pending_Approval/EMAIL_invoice_client.md
---
action: send_email
to: client@example.com
subject: Invoice #2026-001
attachment: invoice.pdf
---
Ready to send. Move to /Approved to proceed.
   ↓
👤 Human reviews and moves to vault/Approved/


Step 4: Execution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Orchestrator detects approved file
   ↓
Calls Email MCP Server
   ↓
Email MCP sends email via Gmail API
   ↓
Logs result to vault/Logs/2026-03-25.json


Step 5: Completion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Move EMAIL_abc123.md to vault/Done/
✅ Move PLAN_invoice_client.md to vault/Done/
✅ Move EMAIL_invoice_client.md to vault/Done/
✅ Update vault/Dashboard.md
📊 Dashboard shows: "Invoice sent to client@example.com ($1,500)"
```

## Process Management Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         WATCHDOG PROCESS                                │
│  Monitors all processes and restarts on failure                        │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  Check every 60 seconds:                                          │ │
│  │  - Is orchestrator running? ✓                                     │ │
│  │  - Is gmail_watcher running? ✓                                    │ │
│  │  - Is whatsapp_watcher running? ✓                                 │ │
│  │  - Is filesystem_watcher running? ✓                               │ │
│  │                                                                   │ │
│  │  If any process crashes → Auto-restart (max 5 times/hour)        │ │
│  │  If restart limit exceeded → Alert human                          │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
         ┌──────────────┐ ┌──────────┐ ┌──────────────┐
         │ Orchestrator │ │ Watchers │ │ MCP Servers  │
         │   (Master)   │ │(Monitors)│ │  (Actions)   │
         └──────────────┘ └──────────┘ └──────────────┘
```

## Security Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SECURITY ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────┘

Layer 1: Credential Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 Environment Variables (.env)
   - GMAIL_CLIENT_ID
   - GMAIL_CLIENT_SECRET
   - BANK_API_TOKEN
   ✓ Never committed to git
   ✓ Rotated monthly

Layer 2: Human-in-the-Loop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Approval Required For:
   - Payments > $100
   - Emails to new contacts
   - Irreversible actions
   - Social media posts
   ✓ File-based approval workflow
   ✓ Explicit human decision

Layer 3: Audit Logging
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Every Action Logged:
   - Timestamp
   - Action type
   - Target
   - Approval status
   - Result
   ✓ 90-day retention
   ✓ JSON format

Layer 4: Dry-Run Mode
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 Test Without Risk:
   - All actions simulated
   - No real emails sent
   - No payments processed
   ✓ Enabled by default
   ✓ Logs show [DRY RUN]

Layer 5: Rate Limiting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ Action Limits:
   - Max 10 emails/hour
   - Max 3 payments/hour
   ✓ Prevents accidents
   ✓ Configurable
```

## Folder Structure Visual

```
vault/
│
├── 📥 Needs_Action/          ← Watchers create files here
│   ├── EMAIL_*.md
│   ├── WHATSAPP_*.md
│   └── FILE_*.md
│
├── ⏳ Pending_Approval/      ← Claude requests approval
│   ├── PAYMENT_*.md
│   └── EMAIL_*.md
│
├── ✅ Approved/              ← Human approves here
│   └── (Files moved from Pending_Approval)
│
├── ❌ Rejected/              ← Human rejects here
│   └── (Files moved from Pending_Approval)
│
├── ✔️ Done/                  ← Completed tasks
│   └── (All completed files archived)
│
├── 📋 Plans/                 ← Claude's action plans
│   └── PLAN_*.md
│
├── 📝 Logs/                  ← Audit trail
│   ├── 2026-03-25.json
│   ├── orchestrator.log
│   └── gmail_watcher.log
│
├── 📊 Briefings/             ← Weekly reports
│   └── 2026-03-25_Monday_Briefing.md
│
├── 💰 Accounting/            ← Financial records
│   └── transactions.csv
│
├── 📁 Drop/                  ← File drop zone
│   └── (Drop files here for processing)
│
├── 📂 Projects/              ← Project files
│   └── project_alpha/
│
├── 👥 Contacts/              ← Contact information
│   └── clients.md
│
├── 📊 Dashboard.md           ← Real-time status
├── 📖 Company_Handbook.md    ← Behavior rules
└── 🎯 Business_Goals.md      ← Objectives & KPIs
```

## Technology Stack Visual

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TECHNOLOGY STACK                                │
└─────────────────────────────────────────────────────────────────────────┘

Frontend/Interface Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Obsidian (Markdown)
   - Dashboard
   - Knowledge base
   - Human interface

AI/Reasoning Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 Claude Code (Opus 4.6)
   - Task reasoning
   - Plan creation
   - Decision making

Backend/Processing Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐍 Python 3.10+
   - Watchers
   - Orchestrator
   - MCP servers
   - Utilities

Integration Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Gmail API (OAuth 2.0)
💬 WhatsApp Web (Playwright)
🌐 Browser Automation (Playwright)
📁 File System (Watchdog)

Infrastructure Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ PM2 (Process Management)
🔄 Watchdog (Health Monitoring)
📊 psutil (System Monitoring)
```

---

**Visual Guide Complete!** 🎨

This document provides visual representations of:
- System architecture and data flow
- Process management structure
- Security layers
- Folder organization
- Technology stack

Use these diagrams in your demo video and documentation!
