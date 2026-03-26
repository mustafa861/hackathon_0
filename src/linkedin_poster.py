"""
LinkedIn Auto-Poster
Automatically posts business updates to LinkedIn to generate sales.
Uses Playwright for browser automation.
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime
import json
import logging

class LinkedInPoster:
    def __init__(self, vault_path: str, session_path: str):
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path)
        self.posts_queue = self.vault_path / 'Social_Posts' / 'LinkedIn_Queue'
        self.posts_done = self.vault_path / 'Social_Posts' / 'LinkedIn_Done'
        self.logger = logging.getLogger(self.__class__.__name__)

        # Create directories if they don't exist
        self.posts_queue.mkdir(parents=True, exist_ok=True)
        self.posts_done.mkdir(parents=True, exist_ok=True)

    def post_to_linkedin(self, post_file: Path) -> bool:
        """Post content to LinkedIn"""
        try:
            # Read post content
            content = post_file.read_text(encoding='utf-8')

            # Extract post text (skip frontmatter)
            lines = content.split('\n')
            post_text = []
            in_frontmatter = False

            for line in lines:
                if line.strip() == '---':
                    in_frontmatter = not in_frontmatter
                    continue
                if not in_frontmatter and line.strip():
                    post_text.append(line)

            post_content = '\n'.join(post_text)

            if not post_content.strip():
                self.logger.error('Post content is empty')
                return False

            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,
                    args=['--no-sandbox']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                self.logger.info('Opening LinkedIn...')
                page.goto('https://www.linkedin.com/feed/', timeout=60000)

                # Wait for feed to load
                page.wait_for_selector('[data-test-id="share-box-open"], .share-box-feed-entry__trigger', timeout=30000)

                # Click "Start a post" button
                start_post_btn = page.query_selector('[data-test-id="share-box-open"], .share-box-feed-entry__trigger')
                if start_post_btn:
                    start_post_btn.click()
                    page.wait_for_timeout(2000)

                    # Find text editor
                    editor = page.query_selector('.ql-editor, [contenteditable="true"]')
                    if editor:
                        # Type post content
                        editor.click()
                        page.wait_for_timeout(1000)
                        editor.fill(post_content)
                        page.wait_for_timeout(2000)

                        # Click Post button
                        post_btn = page.query_selector('button[data-test-share-button="primary-share-action"], button:has-text("Post")')
                        if post_btn:
                            post_btn.click()
                            self.logger.info('Post published successfully!')
                            page.wait_for_timeout(3000)

                            browser.close()
                            return True
                        else:
                            self.logger.error('Post button not found')
                    else:
                        self.logger.error('Editor not found')
                else:
                    self.logger.error('Start post button not found')

                browser.close()
                return False

        except Exception as e:
            self.logger.error(f'Failed to post: {e}')
            return False

    def process_queue(self):
        """Process all posts in queue"""
        post_files = list(self.posts_queue.glob('*.md'))

        if not post_files:
            self.logger.info('No posts in queue')
            return

        self.logger.info(f'Found {len(post_files)} post(s) in queue')

        for post_file in post_files:
            self.logger.info(f'Processing: {post_file.name}')

            if self.post_to_linkedin(post_file):
                # Move to done folder
                done_file = self.posts_done / f'{post_file.stem}_posted_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
                post_file.rename(done_file)
                self.logger.info(f'Moved to done: {done_file.name}')
            else:
                self.logger.error(f'Failed to post: {post_file.name}')

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print('Usage: python linkedin_poster.py <vault_path> <session_path>')
        print('Note: Place post files in vault/Social_Posts/LinkedIn_Queue/')
        sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    poster = LinkedInPoster(sys.argv[1], sys.argv[2])
    poster.process_queue()
