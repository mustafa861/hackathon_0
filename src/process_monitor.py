"""
Watchdog Process
Monitors and restarts critical processes if they crash.
"""

import subprocess
import time
import psutil
from pathlib import Path
import logging
from datetime import datetime

class Watchdog:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.logs = self.vault_path / 'Logs'
        self.logs.mkdir(parents=True, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs / 'watchdog.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Watchdog')

        # Process definitions
        self.processes = {}
        self.restart_counts = {}
        self.max_restarts = 5  # Max restarts per hour

    def add_process(self, name: str, command: list, cwd: str = None):
        """Add a process to monitor"""
        self.processes[name] = {
            'command': command,
            'cwd': cwd,
            'proc': None,
            'pid': None
        }
        self.restart_counts[name] = []

    def is_process_running(self, name: str) -> bool:
        """Check if a process is running"""
        proc_info = self.processes.get(name)
        if not proc_info or not proc_info['pid']:
            return False

        try:
            process = psutil.Process(proc_info['pid'])
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def start_process(self, name: str):
        """Start a process"""
        proc_info = self.processes[name]

        try:
            self.logger.info(f'Starting process: {name}')

            proc = subprocess.Popen(
                proc_info['command'],
                cwd=proc_info['cwd'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            proc_info['proc'] = proc
            proc_info['pid'] = proc.pid

            self.logger.info(f'Process {name} started with PID {proc.pid}')

        except Exception as e:
            self.logger.error(f'Failed to start {name}: {e}')

    def stop_process(self, name: str):
        """Stop a process"""
        proc_info = self.processes.get(name)
        if not proc_info or not proc_info['proc']:
            return

        try:
            self.logger.info(f'Stopping process: {name}')
            proc_info['proc'].terminate()
            proc_info['proc'].wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.logger.warning(f'Force killing {name}')
            proc_info['proc'].kill()
        except Exception as e:
            self.logger.error(f'Error stopping {name}: {e}')

    def can_restart(self, name: str) -> bool:
        """Check if process can be restarted (rate limiting)"""
        now = time.time()
        hour_ago = now - 3600

        # Clean old restart times
        self.restart_counts[name] = [
            t for t in self.restart_counts[name] if t > hour_ago
        ]

        return len(self.restart_counts[name]) < self.max_restarts

    def check_and_restart(self):
        """Check all processes and restart if needed"""
        for name in self.processes:
            if not self.is_process_running(name):
                self.logger.warning(f'Process {name} is not running')

                if self.can_restart(name):
                    self.start_process(name)
                    self.restart_counts[name].append(time.time())
                    self.notify_human(f'Process {name} was restarted')
                else:
                    self.logger.error(f'Process {name} exceeded restart limit')
                    self.notify_human(f'ALERT: {name} crashed too many times')

    def notify_human(self, message: str):
        """Create notification file for human"""
        alert_file = self.vault_path / 'Needs_Action' / f'ALERT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'

        content = f'''---
type: system_alert
priority: high
created: {datetime.now().isoformat()}
---

## System Alert

{message}

**Time**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Please review the system logs for more details.
'''

        alert_file.write_text(content, encoding='utf-8')

    def run(self, check_interval: int = 60):
        """Main watchdog loop"""
        self.logger.info('Watchdog started')

        # Start all processes
        for name in self.processes:
            self.start_process(name)

        try:
            while True:
                self.check_and_restart()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            self.logger.info('Watchdog stopped by user')

            # Stop all processes
            for name in self.processes:
                self.stop_process(name)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python watchdog.py <vault_path>')
        sys.exit(1)

    vault_path = sys.argv[1]

    # Create watchdog
    watchdog = Watchdog(vault_path)

    # Add processes to monitor
    watchdog.add_process(
        'orchestrator',
        ['python', 'orchestrator.py', vault_path],
        cwd=str(Path(__file__).parent)
    )

    watchdog.add_process(
        'gmail_watcher',
        ['python', 'watchers/gmail_watcher.py', vault_path, 'credentials.json'],
        cwd=str(Path(__file__).parent)
    )

    watchdog.add_process(
        'filesystem_watcher',
        ['python', 'watchers/filesystem_watcher.py', vault_path, f'{vault_path}/Drop'],
        cwd=str(Path(__file__).parent)
    )

    # Run watchdog
    watchdog.run()
