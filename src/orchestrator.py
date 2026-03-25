"""
Orchestrator - Master Process
Manages scheduling, folder watching, and Claude Code invocation.
"""

import os
import time
import subprocess
from pathlib import Path
from datetime import datetime
import logging
import json

class Orchestrator:
    def __init__(self, vault_path: str, claude_code_path: str = 'claude'):
        self.vault_path = Path(vault_path)
        self.claude_code_path = claude_code_path
        self.needs_action = self.vault_path / 'Needs_Action'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'

        # Ensure directories exist
        for dir_path in [self.needs_action, self.approved, self.done, self.logs]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs / 'orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Orchestrator')

        self.last_check = {}

    def check_needs_action(self):
        """Check if there are files in Needs_Action folder"""
        files = list(self.needs_action.glob('*.md'))
        return len(files) > 0, files

    def check_approved(self):
        """Check if there are approved actions to execute"""
        files = list(self.approved.glob('*.md'))
        return len(files) > 0, files

    def invoke_claude(self, prompt: str, context_files: list = None):
        """Invoke Claude Code with a prompt"""
        try:
            self.logger.info(f'Invoking Claude Code: {prompt[:100]}...')

            # Build command
            cmd = [self.claude_code_path, '--cwd', str(self.vault_path)]

            # Add context files if provided
            if context_files:
                for file in context_files:
                    cmd.extend(['--file', str(file)])

            # Execute Claude Code
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            self.logger.info(f'Claude Code completed with return code: {result.returncode}')
            return result.returncode == 0

        except subprocess.TimeoutExpired:
            self.logger.error('Claude Code timed out')
            return False
        except Exception as e:
            self.logger.error(f'Failed to invoke Claude Code: {e}')
            return False

    def process_needs_action(self):
        """Process files in Needs_Action folder"""
        has_files, files = self.check_needs_action()

        if not has_files:
            return

        self.logger.info(f'Found {len(files)} files in Needs_Action')

        # Create prompt for Claude
        prompt = f"""You are an AI Employee managing tasks in an Obsidian vault.

Current time: {datetime.now().isoformat()}

TASK: Process all files in the /Needs_Action folder.

For each file:
1. Read and understand the content
2. Create a plan in /Plans folder with actionable steps
3. If the action requires approval (payments, emails to new contacts, etc.), create an approval request in /Pending_Approval
4. If the action is safe to execute automatically, proceed
5. Move the original file to /Done when complete
6. Log all actions to /Logs

IMPORTANT RULES:
- Always require approval for: payments > $50, emails to new contacts, irreversible actions
- Be conservative - when in doubt, ask for approval
- Create detailed plans with checkboxes
- Log everything

Files to process: {len(files)}
"""

        # Invoke Claude with context
        success = self.invoke_claude(prompt, context_files=files[:5])  # Limit context

        if success:
            self.logger.info('Successfully processed Needs_Action folder')
        else:
            self.logger.warning('Claude Code processing may have failed')

    def execute_approved_actions(self):
        """Execute actions that have been approved by human"""
        has_files, files = self.check_approved()

        if not has_files:
            return

        self.logger.info(f'Found {len(files)} approved actions')

        for file in files:
            try:
                # Read approval file
                content = file.read_text(encoding='utf-8')

                # Parse frontmatter to determine action type
                if '---' in content:
                    frontmatter = content.split('---')[1]

                    # Log the approval
                    self.log_action({
                        'timestamp': datetime.now().isoformat(),
                        'action_type': 'approved_action',
                        'file': file.name,
                        'status': 'executing'
                    })

                    # Invoke Claude to execute
                    prompt = f"""Execute the approved action in: {file}

This action has been approved by a human. Please:
1. Read the action details
2. Execute the action using appropriate MCP servers
3. Log the result to /Logs
4. Move the approval file to /Done

File path: {file}
"""

                    success = self.invoke_claude(prompt, context_files=[file])

                    if success:
                        # Move to done
                        done_path = self.done / file.name
                        file.rename(done_path)
                        self.logger.info(f'Executed and archived: {file.name}')

            except Exception as e:
                self.logger.error(f'Failed to execute approved action {file}: {e}')

    def log_action(self, action_data: dict):
        """Log action to daily log file"""
        log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}.json'

        # Load existing logs
        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except:
                logs = []

        # Append new log
        logs.append(action_data)

        # Save
        log_file.write_text(json.dumps(logs, indent=2))

    def run_scheduled_tasks(self):
        """Run scheduled tasks like daily briefings"""
        now = datetime.now()

        # Check if it's time for weekly briefing (Sunday 7 AM)
        if now.weekday() == 6 and now.hour == 7:
            last_briefing = self.last_check.get('weekly_briefing', '')
            today_str = now.strftime('%Y-%m-%d')

            if last_briefing != today_str:
                self.logger.info('Generating weekly CEO briefing')
                self.generate_weekly_briefing()
                self.last_check['weekly_briefing'] = today_str

    def generate_weekly_briefing(self):
        """Generate Monday morning CEO briefing"""
        prompt = """Generate a comprehensive Monday Morning CEO Briefing.

Review:
1. /Accounting folder for revenue and expenses
2. /Done folder for completed tasks this week
3. /Plans folder for any delayed tasks
4. Bank transactions for subscription costs

Create a briefing in /Briefings folder with:
- Revenue summary (week, MTD, trend)
- Completed tasks
- Bottlenecks (tasks with delays)
- Proactive suggestions (cost optimization, upcoming deadlines)

Use the template format from Business_Goals.md
"""

        self.invoke_claude(prompt)

    def run(self, check_interval: int = 60):
        """Main orchestration loop"""
        self.logger.info('Orchestrator started')

        while True:
            try:
                # Check for new items to process
                self.process_needs_action()

                # Execute approved actions
                self.execute_approved_actions()

                # Run scheduled tasks
                self.run_scheduled_tasks()

                # Sleep
                time.sleep(check_interval)

            except KeyboardInterrupt:
                self.logger.info('Orchestrator stopped by user')
                break
            except Exception as e:
                self.logger.error(f'Error in orchestration loop: {e}', exc_info=True)
                time.sleep(check_interval)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python orchestrator.py <vault_path> [claude_code_path]')
        sys.exit(1)

    vault_path = sys.argv[1]
    claude_code_path = sys.argv[2] if len(sys.argv) > 2 else 'claude'

    orchestrator = Orchestrator(vault_path, claude_code_path)
    orchestrator.run()
