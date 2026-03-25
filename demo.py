"""
Demo Script - Personal AI Employee
Demonstrates the system working end-to-end without requiring external credentials.
"""

import time
from pathlib import Path
import sys

print("=" * 80)
print("PERSONAL AI EMPLOYEE - LIVE DEMO")
print("=" * 80)
print()

# Add src to path
sys.path.insert(0, 'src')

from watchers.filesystem_watcher import DropFolderHandler
from watchdog.observers import Observer

vault_path = Path("vault")
drop_path = vault_path / "Drop"
needs_action = vault_path / "Needs_Action"

print("DEMO: File Drop Detection and Processing")
print("-" * 80)
print()

# Step 1: Setup
print("Step 1: Setting up file system watcher...")
event_handler = DropFolderHandler(str(vault_path))
observer = Observer()
observer.schedule(event_handler, str(drop_path), recursive=False)
observer.start()
print(f"   [OK] Watching: {drop_path}")
print()

# Step 2: Create test files
print("Step 2: Creating test files in Drop folder...")
test_files = [
    ("client_invoice.pdf", "Invoice for Client A - $1,500"),
    ("meeting_notes.txt", "Meeting notes from today's standup"),
    ("expense_report.xlsx", "Q1 2026 expense report")
]

for filename, content in test_files:
    file_path = drop_path / filename
    file_path.write_text(content)
    print(f"   [OK] Created: {filename}")

print()
print("Step 3: Waiting for watcher to detect files (3 seconds)...")
time.sleep(3)

# Step 4: Check results
print()
print("Step 4: Checking Needs_Action folder...")
action_files = list(needs_action.glob("FILE_*.md"))

if action_files:
    print(f"   [OK] Found {len(action_files)} action files created!")
    print()

    for action_file in action_files:
        print(f"   --> {action_file.name}")
        content = action_file.read_text(encoding='utf-8')
        # Show first few lines
        lines = content.split('\n')[:10]
        for line in lines:
            print(f"       {line}")
        print()
else:
    print("   [INFO] No action files created yet (watcher may need more time)")

# Step 5: Show workflow
print()
print("Step 5: Next Steps in the Workflow:")
print("-" * 80)
print()
print("1. ORCHESTRATOR would detect these files in Needs_Action/")
print("2. CLAUDE CODE would analyze each file and create plans")
print("3. For sensitive actions, files move to Pending_Approval/")
print("4. HUMAN reviews and moves to Approved/ or Rejected/")
print("5. MCP SERVERS execute approved actions")
print("6. Results logged to Logs/ and files moved to Done/")
print()

# Cleanup
observer.stop()
observer.join()

print("=" * 80)
print("DEMO COMPLETE")
print("=" * 80)
print()
print("WHAT JUST HAPPENED:")
print("- File system watcher detected new files in Drop/")
print("- Created action files in Needs_Action/ with metadata")
print("- System is ready for orchestrator to process them")
print()
print("TO CONTINUE TESTING:")
print("1. Check vault/Needs_Action/ for the created files")
print("2. Run orchestrator: python src/orchestrator.py vault/")
print("3. Monitor vault/Dashboard.md for status updates")
print()
print("NOTE: System is in DRY_RUN mode - safe to test!")
print("=" * 80)
