@echo off
REM Windows Task Scheduler Setup Script
REM Creates scheduled tasks for AI Employee watchers

echo Setting up scheduled tasks for AI Employee...

REM Schedule Gmail Watcher (every 2 minutes)
schtasks /create /tn "AIEmployee_GmailWatcher" /tr "python %CD%\src\watchers\gmail_watcher.py vault\ credentials.json" /sc minute /mo 2 /f

REM Schedule WhatsApp Watcher (every 30 seconds - use PM2 instead)
echo WhatsApp watcher should use PM2 for continuous monitoring

REM Schedule File System Watcher (continuous - use PM2)
echo File System watcher should use PM2 for continuous monitoring

REM Schedule LinkedIn Watcher (every 5 minutes)
schtasks /create /tn "AIEmployee_LinkedInWatcher" /tr "python %CD%\src\watchers\linkedin_watcher.py vault\ .linkedin_session\" /sc minute /mo 5 /f

REM Schedule Facebook Watcher (every 5 minutes)
schtasks /create /tn "AIEmployee_FacebookWatcher" /tr "python %CD%\src\watchers\facebook_watcher.py vault\ .facebook_session\" /sc minute /mo 5 /f

REM Schedule Instagram Watcher (every 5 minutes)
schtasks /create /tn "AIEmployee_InstagramWatcher" /tr "python %CD%\src\watchers\instagram_watcher.py vault\ .instagram_session\" /sc minute /mo 5 /f

REM Schedule Twitter Watcher (every 5 minutes)
schtasks /create /tn "AIEmployee_TwitterWatcher" /tr "python %CD%\src\watchers\twitter_watcher.py vault\ .twitter_session\" /sc minute /mo 5 /f

REM Schedule Orchestrator (every 1 minute)
schtasks /create /tn "AIEmployee_Orchestrator" /tr "python %CD%\src\orchestrator.py vault\" /sc minute /mo 1 /f

echo.
echo Scheduled tasks created successfully!
echo.
echo To view tasks: schtasks /query | findstr AIEmployee
echo To delete tasks: schtasks /delete /tn "AIEmployee_*" /f
echo.
echo Note: For production use, consider using PM2 instead for better process management
pause
