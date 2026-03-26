"""
LinkedIn Watcher
Monitors LinkedIn for messages, connection requests, and post opportunities.
Uses Playwright for browser automation.
"""

from playwright.sync_api import sync_playwright
from base_watcher import BaseWatcher
from pathlib import Path
from datetime import datetime
import json

class LinkedInWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str):
        super().__init__(vault_path, check_interval=300)  # Check every 5 minutes
        self.session_path = Path(session_path)
        self.keywords = ['opportunity', 'collaboration', 'partnership', 'project', 'hire', 'consulting']
        self.processed_items = set()

    def check_for_updates(self) -> list:
        """Check LinkedIn for new messages and connection requests"""
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

                self.logger.info('Opening LinkedIn...')
                page.goto('https://www.linkedin.com/messaging/', timeout=120000)

                # Wait for LinkedIn to load
                try:
                    # Wait for either messaging list or login page
                    page.wait_for_selector('.msg-conversations-container__conversations-list, #session_key', timeout=60000)

                    # Check if we need to login
                    if page.query_selector('#session_key'):
                        self.logger.info('LOGIN REQUIRED - Please login to LinkedIn!')
                        self.logger.info('Waiting up to 3 minutes for you to login...')
                        page.wait_for_selector('.msg-conversations-container__conversations-list', timeout=180000)
                        self.logger.info('Login successful! Checking messages...')
                    else:
                        self.logger.info('Already logged in! Checking messages...')

                    # Check for unread messages
                    unread_convos = page.query_selector_all('.msg-conversation-listitem--unread')

                    for convo in unread_convos[:5]:  # Limit to 5 most recent
                        try:
                            # Click to open conversation
                            convo.click()
                            page.wait_for_timeout(2000)  # Wait for message to load

                            # Get sender name
                            sender_elem = page.query_selector('.msg-entity-lockup__entity-title')
                            sender = sender_elem.inner_text() if sender_elem else 'Unknown'

                            # Get message text
                            msg_elem = page.query_selector('.msg-s-event-listitem__body')
                            text = msg_elem.inner_text().lower() if msg_elem else ''

                            # Check for keywords
                            if any(kw in text for kw in self.keywords) or len(text) > 50:
                                msg_id = f"linkedin_{sender}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if msg_id not in self.processed_items:
                                    items.append({
                                        'id': msg_id,
                                        'type': 'message',
                                        'sender': sender,
                                        'text': text[:300],
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_items.add(msg_id)
                                    self.logger.info(f'Found LinkedIn message from {sender}')

                        except Exception as e:
                            self.logger.error(f'Error processing conversation: {e}')
                            continue

                    # Check for connection requests
                    try:
                        page.goto('https://www.linkedin.com/mynetwork/invitation-manager/', timeout=60000)
                        page.wait_for_timeout(3000)

                        invitations = page.query_selector_all('.invitation-card')

                        for inv in invitations[:3]:  # Limit to 3 most recent
                            try:
                                name_elem = inv.query_selector('.invitation-card__name')
                                name = name_elem.inner_text() if name_elem else 'Unknown'

                                headline_elem = inv.query_selector('.invitation-card__occupation')
                                headline = headline_elem.inner_text() if headline_elem else ''

                                inv_id = f"linkedin_connection_{name}_{datetime.now().strftime('%Y%m%d')}"

                                if inv_id not in self.processed_items:
                                    items.append({
                                        'id': inv_id,
                                        'type': 'connection_request',
                                        'sender': name,
                                        'headline': headline,
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_items.add(inv_id)
                                    self.logger.info(f'Found connection request from {name}')

                            except Exception as e:
                                self.logger.error(f'Error processing invitation: {e}')
                                continue

                    except Exception as e:
                        self.logger.error(f'Error checking connection requests: {e}')

                except Exception as e:
                    self.logger.error(f'Timeout waiting for LinkedIn: {e}')
                    self.logger.info('Browser will stay open - please login manually if needed')
                    import time
                    time.sleep(10)
                    browser.close()
                    return []

                browser.close()

        except Exception as e:
            self.logger.error(f'LinkedIn check failed: {e}')

        return items

    def create_action_file(self, item) -> Path:
        """Create action file for LinkedIn item"""

        if item['type'] == 'message':
            content = f'''---
type: linkedin_message
from: {item['sender']}
received: {item['timestamp']}
priority: high
status: pending
item_id: {item['id']}
---

## LinkedIn Message

**From:** {item['sender']}

**Message Preview:**
{item['text']}

## Suggested Actions
- [ ] Reply to message
- [ ] Schedule a call
- [ ] Add to CRM
- [ ] Create follow-up task

## Keywords Detected
{', '.join([kw for kw in self.keywords if kw in item['text'].lower()])}
'''
        else:  # connection_request
            content = f'''---
type: linkedin_connection
from: {item['sender']}
headline: {item.get('headline', 'N/A')}
received: {item['timestamp']}
priority: medium
status: pending
item_id: {item['id']}
---

## LinkedIn Connection Request

**From:** {item['sender']}
**Headline:** {item.get('headline', 'N/A')}

## Suggested Actions
- [ ] Review profile
- [ ] Accept connection
- [ ] Send personalized message
- [ ] Decline if not relevant

## Decision
- Accept: Yes / No
- Reason: [Add reasoning here]
'''

        # Sanitize filename
        safe_name = ''.join(c for c in item['sender'] if c.isalnum() or c in (' ', '-', '_'))
        filepath = self.needs_action / f'LINKEDIN_{item["type"]}_{safe_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath.write_text(content, encoding='utf-8')

        return filepath

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python linkedin_watcher.py <vault_path> <session_path>')
        print('Note: First run requires manual LinkedIn login')
        sys.exit(1)

    watcher = LinkedInWatcher(sys.argv[1], sys.argv[2])
    watcher.run()
