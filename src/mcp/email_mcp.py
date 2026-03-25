"""
Example MCP Email Server
Handles email sending via Gmail API with approval workflow.
"""

import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('EmailMCP')

class EmailMCP:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = Credentials.from_authorized_user_file(self.credentials_path)
        return build('gmail', 'v1', credentials=creds)

    def send_email(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None):
        """Send an email via Gmail API"""
        try:
            # Check dry run mode
            if os.getenv('DRY_RUN', 'true').lower() == 'true':
                logger.info(f'[DRY RUN] Would send email to {to}')
                logger.info(f'[DRY RUN] Subject: {subject}')
                logger.info(f'[DRY RUN] Body preview: {body[:100]}...')
                return {'status': 'dry_run', 'message': 'Email not sent (dry run mode)'}

            # Create message
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject

            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc

            # Add body
            msg_body = MIMEText(body, 'plain')
            message.attach(msg_body)

            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            # Send
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            logger.info(f'Email sent successfully. Message ID: {result["id"]}')
            return {'status': 'success', 'message_id': result['id']}

        except Exception as e:
            logger.error(f'Failed to send email: {e}')
            return {'status': 'error', 'error': str(e)}

    def draft_email(self, to: str, subject: str, body: str):
        """Create a draft email"""
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': {'raw': raw_message}}
            ).execute()

            logger.info(f'Draft created. Draft ID: {draft["id"]}')
            return {'status': 'success', 'draft_id': draft['id']}

        except Exception as e:
            logger.error(f'Failed to create draft: {e}')
            return {'status': 'error', 'error': str(e)}

    def search_emails(self, query: str, max_results: int = 10):
        """Search emails by query"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            logger.info(f'Found {len(messages)} messages matching query: {query}')

            return {'status': 'success', 'count': len(messages), 'messages': messages}

        except Exception as e:
            logger.error(f'Failed to search emails: {e}')
            return {'status': 'error', 'error': str(e)}

# MCP Server Interface
def handle_tool_call(tool_name: str, parameters: dict):
    """Handle MCP tool calls"""
    credentials_path = os.getenv('GMAIL_CREDENTIALS', 'credentials.json')
    email_mcp = EmailMCP(credentials_path)

    if tool_name == 'send_email':
        return email_mcp.send_email(
            to=parameters['to'],
            subject=parameters['subject'],
            body=parameters['body'],
            cc=parameters.get('cc'),
            bcc=parameters.get('bcc')
        )

    elif tool_name == 'draft_email':
        return email_mcp.draft_email(
            to=parameters['to'],
            subject=parameters['subject'],
            body=parameters['body']
        )

    elif tool_name == 'search_emails':
        return email_mcp.search_emails(
            query=parameters['query'],
            max_results=parameters.get('max_results', 10)
        )

    else:
        return {'status': 'error', 'error': f'Unknown tool: {tool_name}'}

if __name__ == '__main__':
    # Test the MCP server
    print("Email MCP Server - Test Mode")

    # Test send email
    result = handle_tool_call('send_email', {
        'to': 'test@example.com',
        'subject': 'Test Email',
        'body': 'This is a test email from the AI Employee system.'
    })

    print(json.dumps(result, indent=2))
