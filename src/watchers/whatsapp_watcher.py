"""
WhatsApp Watcher
Monitors WhatsApp Web for urgent messages using Playwright.
WARNING: Use responsibly and be aware of WhatsApp's terms of service.
"""

from playwright.sync_api import sync_playwright
from base_watcher import BaseWatcher
from pathlib import Path
from datetime import datetime
import json

class WhatsAppWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str):
        super().__init__(vault_path, check_interval=30)
        self.session_path = Path(session_path)
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'emergency']
        self.processed_messages = set()

    def check_for_updates(self) -> list:
        """Check WhatsApp Web for unread messages with keywords"""
        messages = []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    args=['--no-sandbox']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto('https://web.whatsapp.com', timeout=60000)

                # Wait for WhatsApp to load
                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                except:
                    self.logger.warning('WhatsApp not loaded, may need manual login')
                    browser.close()
                    return []

                # Find unread chats
                unread_chats = page.query_selector_all('[aria-label*="unread"]')

                for chat in unread_chats[:5]:  # Limit to 5 most recent
                    try:
                        text = chat.inner_text().lower()

                        # Check for keywords
                        if any(kw in text for kw in self.keywords):
                            # Extract chat name
                            chat_name = chat.query_selector('[dir="auto"]')
                            name = chat_name.inner_text() if chat_name else 'Unknown'

                            # Create unique ID
                            msg_id = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                            if msg_id not in self.processed_messages:
                                messages.append({
                                    'id': msg_id,
                                    'name': name,
                                    'text': text[:200],
                                    'timestamp': datetime.now().isoformat()
                                })
                                self.processed_messages.add(msg_id)
                    except Exception as e:
                        self.logger.error(f'Error processing chat: {e}')
                        continue

                browser.close()
        except Exception as e:
            self.logger.error(f'WhatsApp check failed: {e}')

        return messages

    def create_action_file(self, message) -> Path:
        """Create action file for WhatsApp message"""
        content = f'''---
type: whatsapp
from: {message['name']}
received: {message['timestamp']}
priority: high
status: pending
message_id: {message['id']}
---

## Message Preview
{message['text']}

## Suggested Actions
- [ ] Reply to sender
- [ ] Create task or reminder
- [ ] Forward to relevant party
- [ ] Archive after processing

## Keywords Detected
{', '.join([kw for kw in self.keywords if kw in message['text'].lower()])}
'''

        # Sanitize filename
        safe_name = ''.join(c for c in message['name'] if c.isalnum() or c in (' ', '-', '_'))
        filepath = self.needs_action / f'WHATSAPP_{safe_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath.write_text(content, encoding='utf-8')

        return filepath

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python whatsapp_watcher.py <vault_path> <session_path>')
        print('Note: First run requires manual WhatsApp Web login')
        sys.exit(1)

    watcher = WhatsAppWatcher(sys.argv[1], sys.argv[2])
    watcher.run()
