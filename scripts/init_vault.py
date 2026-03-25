"""
Vault Initialization Script
Creates the required folder structure and template files for the AI Employee system.
"""

import os
from pathlib import Path
import sys

def create_vault_structure(vault_path: str):
    """Create the complete vault folder structure"""
    vault = Path(vault_path)

    # Define folder structure
    folders = [
        'Needs_Action',
        'Pending_Approval',
        'Approved',
        'Rejected',
        'Done',
        'Plans',
        'Logs',
        'Briefings',
        'Accounting',
        'Drop',
        'Projects',
        'Contacts'
    ]

    print(f"Creating vault structure at: {vault.absolute()}")

    # Create folders
    for folder in folders:
        folder_path = vault / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {folder}/")

        # Create .gitkeep to preserve empty folders
        gitkeep = folder_path / '.gitkeep'
        gitkeep.touch()

    # Create README files for key folders
    create_folder_readmes(vault)

    print("\n✓ Vault structure created successfully!")
    print(f"\nVault location: {vault.absolute()}")
    print("\nNext steps:")
    print("1. Review and customize vault/Business_Goals.md")
    print("2. Review and customize vault/Company_Handbook.md")
    print("3. Setup credentials in .env file")
    print("4. Start the watchers: python src/watchdog.py vault/")

def create_folder_readmes(vault: Path):
    """Create README files explaining each folder's purpose"""

    readmes = {
        'Needs_Action': """# Needs Action

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
""",

        'Pending_Approval': """# Pending Approval

Actions that require human approval before execution.

## How to approve
1. Review the action file
2. Move to ../Approved/ to proceed
3. Or move to ../Rejected/ to cancel

## What requires approval
- Payments > $100
- Emails to new contacts
- Irreversible actions
- Social media posts
- File deletions
""",

        'Approved': """# Approved

Actions approved by human, ready for execution.

## Process
1. Orchestrator detects files here
2. Invokes Claude Code to execute
3. Logs the result
4. Moves to ../Done/
""",

        'Done': """# Done

Completed tasks and executed actions.

Archive of all processed items for audit trail.
""",

        'Plans': """# Plans

AI-generated action plans with step-by-step tasks.

Each plan includes:
- Objective
- Steps with checkboxes
- Required approvals
- Expected completion time
""",

        'Logs': """# Logs

Audit trail of all AI actions.

## Format
- Daily JSON files: YYYY-MM-DD.json
- Watcher logs: <watcher_name>.log
- Orchestrator log: orchestrator.log
- Watchdog log: watchdog.log

## Retention
- Keep logs for minimum 90 days
- Review weekly for anomalies
""",

        'Briefings': """# Briefings

Weekly CEO briefings and reports.

Generated every Sunday night with:
- Revenue summary
- Completed tasks
- Bottlenecks
- Proactive suggestions
""",

        'Drop': """# Drop Folder

Drop files here for AI processing.

The file system watcher monitors this folder and creates action items
for any new files.
"""
    }

    for folder, content in readmes.items():
        readme_path = vault / folder / 'README.md'
        readme_path.write_text(content.strip(), encoding='utf-8')
        print(f"  ✓ Created README in {folder}/")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python init_vault.py <vault_path>")
        print("Example: python init_vault.py vault/")
        sys.exit(1)

    vault_path = sys.argv[1]
    create_vault_structure(vault_path)
