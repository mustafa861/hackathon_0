"""
Instagram Watcher
Monitors Instagram for messages and DMs.
Uses Playwright for browser automation.
"""

from playwright.sync_api import sync_playwright
from base_watcher import BaseWatcher
from pathlib import Path
from datetime import datetime
import json

class InstagramWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str):
        super().__init__(vault_path, check_interval=300)  # Check every 5 minutes
        self.session_path = Path(session_path)
        self.keywords = ['order', 'inquiry', 'interested', 'price', 'buy', 'purchase', 'question']
        self.processed_items = set()

    def check_for_updates(self) -> list:
        """Check Instagram for new messages"""
        items = []

        try:
            with sync_playwright() as p:
                # Check if session exists
                session_exists = self.session_path.exists() and any(self.session_path.iterdir())

                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # Show browser for easier debugging
                    args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                self.logger.info('Opening Instagram...')
                page.goto('https://www.instagram.com/direct/inbox/', timeout=120000)

                # Wait for Instagram to load
                try:
                    # Wait for either messages or login page
                    page.wait_for_selector('[role="main"], input[name="username"]', timeout=60000)

                    # Check if we need to login
                    if page.query_selector('input[name="username"]'):
                        self.logger.info('LOGIN REQUIRED - Please login to Instagram!')
                        self.logger.info('Waiting up to 3 minutes for you to login...')
                        page.wait_for_selector('[role="main"]', timeout=180000)
                        self.logger.info('Login successful! Checking messages...')
                    else:
                        self.logger.info('Already logged in! Checking messages...')

                    # Check for unread messages
                    page.wait_for_timeout(3000)  # Wait for messages to load

                    # Look for unread message indicators
                    unread_indicators = page.query_selector_all('[aria-label*="unread"], [role="listitem"]')

                    for indicator in unread_indicators[:5]:  # Limit to 5 most recent
                        try:
                            # Click to open conversation
                            indicator.click()
                            page.wait_for_timeout(2000)

                            # Get sender name
                            sender_elem = page.query_selector('header a, header span')
                            sender = sender_elem.inner_text() if sender_elem else 'Unknown'

                            # Get message text
                            msg_elems = page.query_selector_all('[dir="auto"]')
                            text = ''
                            for elem in msg_elems[-3:]:  # Get last 3 messages
                                try:
                                    text += elem.inner_text() + ' '
                                except:
                                    continue
                            text = text.lower()

                            # Check for keywords or substantial message
                            if any(kw in text for kw in self.keywords) or len(text) > 30:
                                msg_id = f"instagram_{sender}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if msg_id not in self.processed_items:
                                    items.append({
                                        'id': msg_id,
                                        'type': 'instagram_message',
                                        'sender': sender,
                                        'text': text[:300],
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_items.add(msg_id)
                                    self.logger.info(f'Found Instagram message from {sender}')

                        except Exception as e:
                            self.logger.error(f'Error processing message: {e}')
                            continue

                except Exception as e:
                    self.logger.error(f'Timeout waiting for Instagram: {e}')
                    self.logger.info('Browser will stay open - please login manually if needed')
                    import time
                    time.sleep(10)
                    browser.close()
                    return []

                browser.close()

        except Exception as e:
            self.logger.error(f'Instagram check failed: {e}')

        return items

    def create_action_file(self, item) -> Path:
        """Create action file for Instagram item"""

        content = f'''---
type: instagram_message
platform: Instagram
from: {item['sender']}
received: {item['timestamp']}
priority: high
status: pending
item_id: {item['id']}
---

## Instagram Message

**From:** {item['sender']}

**Message Preview:**
{item['text']}

## Suggested Actions
- [ ] Reply to message
- [ ] Check if it's a sales inquiry
- [ ] Add to CRM
- [ ] Create follow-up task
- [ ] Archive after processing

## Keywords Detected
{', '.join([kw for kw in self.keywords if kw in item['text'].lower()])}

## Notes
Add any relevant context or decisions here.
'''

        # Sanitize filename
        safe_name = ''.join(c for c in item['sender'] if c.isalnum() or c in (' ', '-', '_'))
        filepath = self.needs_action / f'IG_{safe_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath.write_text(content, encoding='utf-8')

        return filepath

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python instagram_watcher.py <vault_path> <session_path>')
        print('Note: First run requires manual Instagram login')
        sys.exit(1)

    watcher = InstagramWatcher(sys.argv[1], sys.argv[2])
    watcher.run()
