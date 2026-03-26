"""
Facebook Watcher
Monitors Facebook for messages, comments, and post opportunities.
Uses Playwright for browser automation.
"""

from playwright.sync_api import sync_playwright
from base_watcher import BaseWatcher
from pathlib import Path
from datetime import datetime
import json

class FacebookWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str):
        super().__init__(vault_path, check_interval=30)  # Check every 30 seconds
        self.session_path = Path(session_path)
        self.keywords = ['order', 'inquiry', 'interested', 'price', 'buy', 'purchase', 'question']
        self.processed_items = set()
        self.playwright = None
        self.browser = None

    def _init_browser(self):
        """Initialize browser if not already initialized"""
        if self.playwright is None:
            self.playwright = sync_playwright().start()
            session_exists = self.session_path.exists() and any(self.session_path.iterdir())
            self.browser = self.playwright.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,  # Always show browser
                args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
            )
            self.logger.info('Browser initialized - will stay open')

    def check_for_updates(self) -> list:
        """Check Facebook for new messages and notifications"""
        items = []

        try:
            # Initialize browser if needed
            self._init_browser()

            page = self.browser.pages[0] if self.browser.pages else self.browser.new_page()

            self.logger.info('Opening Facebook...')
            page.goto('https://www.facebook.com/messages', timeout=180000)

            # Wait for Facebook to load
            try:
                # Wait for either messages or login page
                page.wait_for_selector('[role="navigation"], #email', timeout=120000)

                # Check if we need to login
                if page.query_selector('#email'):
                    self.logger.info('LOGIN REQUIRED - Please login to Facebook!')
                    self.logger.info('Waiting up to 5 minutes for you to login...')
                    page.wait_for_selector('[role="navigation"]', timeout=300000)
                    self.logger.info('Login successful! Checking messages...')
                else:
                    self.logger.info('Already logged in! Checking messages...')

                # Check for unread messages
                page.wait_for_timeout(5000)  # Wait for messages to load

                # Look for unread message indicators
                unread_indicators = page.query_selector_all('[aria-label*="unread"], [aria-label*="Unread"]')

                for indicator in unread_indicators[:5]:  # Limit to 5 most recent
                    try:
                        # Click to open conversation
                        indicator.click()
                        page.wait_for_timeout(2000)

                        # Get sender name
                        sender_elem = page.query_selector('h1, [role="heading"]')
                        sender = sender_elem.inner_text() if sender_elem else 'Unknown'

                        # Get message text
                        msg_elems = page.query_selector_all('[dir="auto"]')
                        text = ''
                        for elem in msg_elems[-3:]:  # Get last 3 messages
                            text += elem.inner_text() + ' '
                        text = text.lower()

                        # Check for keywords or substantial message
                        if any(kw in text for kw in self.keywords) or len(text) > 30:
                            msg_id = f"facebook_{sender}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                            if msg_id not in self.processed_items:
                                items.append({
                                    'id': msg_id,
                                    'type': 'facebook_message',
                                    'sender': sender,
                                    'text': text[:300],
                                    'timestamp': datetime.now().isoformat()
                                })
                                self.processed_items.add(msg_id)
                                self.logger.info(f'Found Facebook message from {sender}')

                    except Exception as e:
                        self.logger.error(f'Error processing message: {e}')
                        continue

            except Exception as e:
                self.logger.error(f'Timeout waiting for Facebook: {e}')
                self.logger.info('Browser will stay open - please login manually if needed')
                import time
                time.sleep(10)
                # Don't close browser - let it stay open
                return []

            # Don't close browser - let it stay open for continuous monitoring
            self.logger.info('Check complete - browser staying open for next check')
            return items

        except Exception as e:
            self.logger.error(f'Facebook check failed: {e}')
            return []

    def create_action_file(self, item) -> Path:
        """Create action file for Facebook item"""

        content = f'''---
type: facebook_message
platform: Facebook
from: {item['sender']}
received: {item['timestamp']}
priority: high
status: pending
item_id: {item['id']}
---

## Facebook Message

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
        filepath = self.needs_action / f'FB_{safe_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath.write_text(content, encoding='utf-8')

        return filepath

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python facebook_watcher.py <vault_path> <session_path>')
        print('Note: First run requires manual Facebook login')
        sys.exit(1)

    watcher = FacebookWatcher(sys.argv[1], sys.argv[2])
    watcher.run()
