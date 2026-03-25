"""
Gmail Watcher
Monitors Gmail inbox for important/unread emails and creates action files.
"""

import os
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from base_watcher import BaseWatcher

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: str, credentials_path: str):
        super().__init__(vault_path, check_interval=120)
        self.credentials_path = credentials_path
        self.token_path = Path(vault_path) / '.gmail_token.pickle'
        self.service = self._authenticate()
        self.processed_ids = set()

    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        # Load existing token
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def check_for_updates(self) -> list:
        """Check for unread important emails"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])
            return [m for m in messages if m['id'] not in self.processed_ids]
        except Exception as e:
            self.logger.error(f'Failed to fetch emails: {e}')
            return []

    def create_action_file(self, message) -> Path:
        """Create markdown file for email"""
        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}

            # Get email body
            body = self._get_body(msg['payload'])

            content = f'''---
type: email
from: {headers.get('From', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
priority: high
status: pending
message_id: {message['id']}
---

## Email Content
{body[:500]}...

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
'''

            filepath = self.needs_action / f'EMAIL_{message["id"]}.md'
            filepath.write_text(content, encoding='utf-8')
            self.processed_ids.add(message['id'])

            return filepath
        except Exception as e:
            self.logger.error(f'Failed to create action file: {e}')
            raise

    def _get_body(self, payload):
        """Extract email body from payload"""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    import base64
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        elif 'body' in payload and 'data' in payload['body']:
            import base64
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        return msg.get('snippet', '')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python gmail_watcher.py <vault_path> <credentials_path>')
        sys.exit(1)

    watcher = GmailWatcher(sys.argv[1], sys.argv[2])
    watcher.run()
