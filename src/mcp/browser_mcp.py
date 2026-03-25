"""
Browser MCP Server
Handles browser automation for payments and web interactions using Playwright.
"""

import os
import logging
from playwright.sync_api import sync_playwright
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('BrowserMCP')

class BrowserMCP:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.dry_run = os.getenv('DRY_RUN', 'true').lower() == 'true'

    def navigate_and_fill(self, url: str, actions: list):
        """
        Navigate to URL and perform actions.

        Actions format:
        [
            {'type': 'fill', 'selector': '#email', 'value': 'user@example.com'},
            {'type': 'click', 'selector': '#submit'},
            {'type': 'wait', 'selector': '.success-message'}
        ]
        """
        if self.dry_run:
            logger.info(f'[DRY RUN] Would navigate to {url}')
            logger.info(f'[DRY RUN] Would perform {len(actions)} actions')
            for i, action in enumerate(actions):
                logger.info(f'[DRY RUN] Action {i+1}: {action["type"]} - {action.get("selector", "N/A")}')
            return {'status': 'dry_run', 'message': 'Actions not performed (dry run mode)'}

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()

                logger.info(f'Navigating to {url}')
                page.goto(url)

                for action in actions:
                    action_type = action['type']

                    if action_type == 'fill':
                        logger.info(f'Filling {action["selector"]}')
                        page.fill(action['selector'], action['value'])

                    elif action_type == 'click':
                        logger.info(f'Clicking {action["selector"]}')
                        page.click(action['selector'])

                    elif action_type == 'wait':
                        logger.info(f'Waiting for {action["selector"]}')
                        page.wait_for_selector(action['selector'], timeout=action.get('timeout', 30000))

                    elif action_type == 'screenshot':
                        screenshot_path = action.get('path', 'screenshot.png')
                        logger.info(f'Taking screenshot: {screenshot_path}')
                        page.screenshot(path=screenshot_path)

                    elif action_type == 'wait_time':
                        import time
                        time.sleep(action.get('seconds', 1))

                # Take final screenshot for verification
                page.screenshot(path='vault/Logs/browser_final.png')

                browser.close()

                logger.info('Browser automation completed successfully')
                return {'status': 'success', 'message': 'Actions completed'}

        except Exception as e:
            logger.error(f'Browser automation failed: {e}')
            return {'status': 'error', 'error': str(e)}

    def make_payment(self, payment_url: str, amount: float, recipient: str, credentials: dict):
        """
        Automated payment workflow (REQUIRES APPROVAL).

        This is a template - customize for your payment provider.
        """
        if self.dry_run:
            logger.info(f'[DRY RUN] Would make payment of ${amount} to {recipient}')
            return {'status': 'dry_run', 'message': 'Payment not made (dry run mode)'}

        logger.warning('PAYMENT AUTOMATION - USE WITH EXTREME CAUTION')

        # Define payment workflow
        actions = [
            {'type': 'fill', 'selector': '#username', 'value': credentials.get('username')},
            {'type': 'fill', 'selector': '#password', 'value': credentials.get('password')},
            {'type': 'click', 'selector': '#login-button'},
            {'type': 'wait', 'selector': '.dashboard'},
            {'type': 'click', 'selector': '#new-payment'},
            {'type': 'fill', 'selector': '#recipient', 'value': recipient},
            {'type': 'fill', 'selector': '#amount', 'value': str(amount)},
            {'type': 'screenshot', 'path': 'vault/Logs/payment_preview.png'},
            # STOP HERE - Do not click submit without explicit approval
        ]

        result = self.navigate_and_fill(payment_url, actions)

        if result['status'] == 'success':
            logger.info('Payment form filled. MANUAL REVIEW REQUIRED before submission.')
            return {
                'status': 'pending_review',
                'message': 'Payment form filled, awaiting manual confirmation',
                'screenshot': 'vault/Logs/payment_preview.png'
            }

        return result

    def scrape_data(self, url: str, selectors: dict):
        """
        Scrape data from a webpage.

        selectors format: {'field_name': 'css_selector'}
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()

                logger.info(f'Scraping data from {url}')
                page.goto(url)

                data = {}
                for field, selector in selectors.items():
                    try:
                        element = page.query_selector(selector)
                        if element:
                            data[field] = element.inner_text()
                        else:
                            data[field] = None
                            logger.warning(f'Selector not found: {selector}')
                    except Exception as e:
                        logger.error(f'Error scraping {field}: {e}')
                        data[field] = None

                browser.close()

                logger.info(f'Scraped {len(data)} fields')
                return {'status': 'success', 'data': data}

        except Exception as e:
            logger.error(f'Scraping failed: {e}')
            return {'status': 'error', 'error': str(e)}

# MCP Server Interface
def handle_tool_call(tool_name: str, parameters: dict):
    """Handle MCP tool calls"""
    headless = os.getenv('HEADLESS', 'true').lower() == 'true'
    browser_mcp = BrowserMCP(headless=headless)

    if tool_name == 'navigate_and_fill':
        return browser_mcp.navigate_and_fill(
            url=parameters['url'],
            actions=parameters['actions']
        )

    elif tool_name == 'make_payment':
        return browser_mcp.make_payment(
            payment_url=parameters['payment_url'],
            amount=parameters['amount'],
            recipient=parameters['recipient'],
            credentials=parameters['credentials']
        )

    elif tool_name == 'scrape_data':
        return browser_mcp.scrape_data(
            url=parameters['url'],
            selectors=parameters['selectors']
        )

    else:
        return {'status': 'error', 'error': f'Unknown tool: {tool_name}'}

if __name__ == '__main__':
    # Test the MCP server
    print("Browser MCP Server - Test Mode")

    # Test scraping
    result = handle_tool_call('scrape_data', {
        'url': 'https://example.com',
        'selectors': {
            'title': 'h1',
            'description': 'p'
        }
    })

    print(json.dumps(result, indent=2))
