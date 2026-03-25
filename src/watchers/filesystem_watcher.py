"""
File System Watcher
Monitors a drop folder for new files and creates action items.
"""

import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

class DropFolderHandler(FileSystemEventHandler):
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger('DropFolderHandler')

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Ignore hidden files and temp files
        if source.name.startswith('.') or source.name.startswith('~'):
            return

        try:
            # Copy file to vault
            dest = self.needs_action / f'FILE_{source.name}'
            shutil.copy2(source, dest)

            # Create metadata file
            self.create_metadata(source, dest)

            self.logger.info(f'Processed new file: {source.name}')
        except Exception as e:
            self.logger.error(f'Failed to process file {source}: {e}')

    def create_metadata(self, source: Path, dest: Path):
        """Create markdown metadata file"""
        meta_path = dest.with_suffix(dest.suffix + '.md')

        content = f'''---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size}
created: {datetime.now().isoformat()}
status: pending
---

## File Information
- **Name**: {source.name}
- **Size**: {source.stat().st_size} bytes
- **Type**: {source.suffix}

## Suggested Actions
- [ ] Review file contents
- [ ] Process or categorize
- [ ] Move to appropriate folder
'''

        meta_path.write_text(content, encoding='utf-8')

def start_filesystem_watcher(vault_path: str, watch_path: str):
    """Start watching a directory for new files"""
    event_handler = DropFolderHandler(vault_path)
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=False)
    observer.start()

    logger = logging.getLogger('FilesystemWatcher')
    logger.info(f'Watching directory: {watch_path}')

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info('Stopped watching')

    observer.join()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python filesystem_watcher.py <vault_path> <watch_path>')
        sys.exit(1)

    start_filesystem_watcher(sys.argv[1], sys.argv[2])
