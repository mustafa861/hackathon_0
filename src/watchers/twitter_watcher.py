"""
Twitter/X Watcher
Monitors Twitter/X for mentions, DMs, and post opportunities.
Uses Playwright for browser automation.
"""

from playwright.sync_api import sync_playwright
from base_watcher import BaseWatcher
from pathlib import Path
from datetime import datetime
import json

class TwitterWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str):
        super().__init__(vault_path, check_interval=30)  # Check every 30 seconds
        self.session_path = Path(session_path)
        self.keywords = ['question', 'help', 'inquiry', 'interested', 'collaboration', 'opportunity']
        self.processed_items = set()

    def check_for_updates(self) -> list:
        """Check Twitter/X for new mentions and DMs"""
        items = []

        try:
            with sync_playwright() as p:
                # Check if session exists
                session_exists = self.session_path.exists() and any(self.session_path.iterdir())

                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=session_exists,  # Show browser only for first login
                    args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                self.logger.info('Opening Twitter/X...')
                page.goto('https://twitter.com/messages', timeout=120000)

                # Wait for Twitter to load
                try:
                    # Wait for either messages or login page
                    page.wait_for_selector('[data-testid="DM_Conversation_Avatar"], input[name="text"]', timeout=60000)

                    # Check if we need to login
                    if page.query_selector('input[name="text"]'):
                        self.logger.info('LOGIN REQUIRED - Please login to Twitter/X!')
                        self.logger.info('Waiting up to 3 minutes for you to login...')
                        page.wait_for_selector('[data-testid="DM_Conversation_Avatar"]', timeout=180000)
                        self.logger.info('Login successful! Checking messages...')
                    else:
                        self.logger.info('Already logged in! Checking messages...')

                    # Check for unread DMs
                    page.wait_for_timeout(3000)  # Wait for messages to load

                    # Look for unread message indicators
                    conversations = page.query_selector_all('[data-testid="conversation"]')

                    for convo in conversations[:5]:  # Limit to 5 most recent
                        try:
                            # Check if unread (has badge or bold text)
                            is_unread = convo.query_selector('[data-testid="badge"]')

                            if is_unread:
                                # Click to open conversation
                                convo.click()
                                page.wait_for_timeout(2000)

                                # Get sender name
                                sender_elem = page.query_selector('[data-testid="User-Name"]')
                                sender = sender_elem.inner_text() if sender_elem else 'Unknown'

                                # Get message text
                                msg_elems = page.query_selector_all('[data-testid="tweetText"]')
                                text = ''
                                for elem in msg_elems[-3:]:  # Get last 3 messages
                                    text += elem.inner_text() + ' '
                                text = text.lower()

                                # Check for keywords or substantial message
                                if any(kw in text for kw in self.keywords) or len(text) > 30:
                                    msg_id = f"twitter_dm_{sender}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                    if msg_id not in self.processed_items:
                                        items.append({
                                            'id': msg_id,
                                            'type': 'twitter_dm',
                                            'sender': sender,
                                            'text': text[:300],
                                            'timestamp': datetime.now().isoformat()
                                        })
                                        self.processed_items.add(msg_id)
                                        self.logger.info(f'Found Twitter DM from {sender}')

                        except Exception as e:
                            self.logger.error(f'Error processing conversation: {e}')
                            continue

                    # Check for mentions
                    try:
                        self.logger.info('Checking mentions...')
                        page.goto('https://twitter.com/notifications/mentions', timeout=60000)
                        page.wait_for_timeout(3000)

                        # Look for recent mentions
                        mentions = page.query_selector_all('[data-testid="tweet"]')

                        for mention in mentions[:5]:  # Limit to 5
                            try:
                                # Get username
                                username_elem = mention.query_selector('[data-testid="User-Name"]')
                                username = username_elem.inner_text() if username_elem else 'Unknown'

                                # Get tweet text
                                text_elem = mention.query_selector('[data-testid="tweetText"]')
                                text = text_elem.inner_text().lower() if text_elem else ''

                                # Check for keywords
                                if any(kw in text for kw in self.keywords):
                                    mention_id = f"twitter_mention_{username}_{datetime.now().strftime('%Y%m%d_%H%M')}"

                                    if mention_id not in self.processed_items:
                                        items.append({
                                            'id': mention_id,
                                            'type': 'twitter_mention',
                                            'sender': username,
                                            'text': text[:300],
                                            'timestamp': datetime.now().isoformat()
                                        })
                                        self.processed_items.add(mention_id)
                                        self.logger.info(f'Found Twitter mention from {username}')

                            except Exception as e:
                                self.logger.error(f'Error processing mention: {e}')
                                continue

                    except Exception as e:
                        self.logger.error(f'Error checking mentions: {e}')

                except Exception as e:
                    self.logger.error(f'Timeout waiting for Twitter: {e}')
                    self.logger.info('Browser will stay open - please login manually if needed')
                    import time
                    time.sleep(10)
                    browser.close()
                    return []

                browser.close()

        except Exception as e:
            self.logger.error(f'Twitter check failed: {e}')

        return items

    def create_action_file(self, item) -> Path:
        """Create action file for Twitter item"""

        item_type = 'Direct Message' if item['type'] == 'twitter_dm' else 'Mention'

        content = f'''---
type: {item['type']}
platform: Twitter/X
from: {item['sender']}
received: {item['timestamp']}
priority: high
status: pending
item_id: {item['id']}
---

## Twitter/X {item_type}

**From:** {item['sender']}

**Message Preview:**
{item['text']}

## Suggested Actions
- [ ] Reply to {item_type.lower()}
- [ ] Like/Retweet if appropriate
- [ ] Add to engagement list
- [ ] Create follow-up task
- [ ] Archive after processing

## Keywords Detected
{', '.join([kw for kw in self.keywords if kw in item['text'].lower()])}

## Notes
Add any relevant context or decisions here.
'''

        # Sanitize filename
        safe_name = ''.join(c for c in item['sender'] if c.isalnum() or c in (' ', '-', '_'))
        type_prefix = 'TW_DM' if item['type'] == 'twitter_dm' else 'TW_MENTION'
        filepath = self.needs_action / f'{type_prefix}_{safe_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath.write_text(content, encoding='utf-8')

        return filepath

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python twitter_watcher.py <vault_path> <session_path>')
        print('Note: First run requires manual Twitter/X login')
        sys.exit(1)

    watcher = TwitterWatcher(sys.argv[1], sys.argv[2])
    watcher.run()
