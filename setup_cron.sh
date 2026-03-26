#!/bin/bash
# Cron Setup Script for AI Employee
# Sets up cron jobs for scheduled tasks

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Setting up cron jobs for AI Employee..."

# Create cron entries
CRON_ENTRIES="
# AI Employee Scheduled Tasks
*/2 * * * * cd $SCRIPT_DIR && python src/watchers/gmail_watcher.py vault/ credentials.json >> vault/Logs/gmail-cron.log 2>&1
*/5 * * * * cd $SCRIPT_DIR && python src/watchers/linkedin_watcher.py vault/ .linkedin_session/ >> vault/Logs/linkedin-cron.log 2>&1
*/5 * * * * cd $SCRIPT_DIR && python src/watchers/facebook_watcher.py vault/ .facebook_session/ >> vault/Logs/facebook-cron.log 2>&1
*/5 * * * * cd $SCRIPT_DIR && python src/watchers/instagram_watcher.py vault/ .instagram_session/ >> vault/Logs/instagram-cron.log 2>&1
*/5 * * * * cd $SCRIPT_DIR && python src/watchers/twitter_watcher.py vault/ .twitter_session/ >> vault/Logs/twitter-cron.log 2>&1
* * * * * cd $SCRIPT_DIR && python src/orchestrator.py vault/ >> vault/Logs/orchestrator-cron.log 2>&1
"

# Backup existing crontab
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null

# Add new entries (remove old AI Employee entries first)
(crontab -l 2>/dev/null | grep -v "AI Employee"; echo "$CRON_ENTRIES") | crontab -

echo "Cron jobs installed successfully!"
echo ""
echo "To view cron jobs: crontab -l"
echo "To remove AI Employee cron jobs: crontab -l | grep -v 'AI Employee' | crontab -"
echo ""
echo "Note: For continuous watchers (WhatsApp, File System), use PM2 instead"
echo "      PM2 provides better process management and auto-restart"
