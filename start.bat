@echo off
REM Quick start script for Personal AI Employee (Windows)
REM Run this after initial setup to start all components

echo.
echo 🤖 Personal AI Employee - Quick Start
echo ======================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.10+
    exit /b 1
)
echo ✓ Python installed
echo.

REM Check if vault exists
if not exist "vault" (
    echo 📁 Initializing vault structure...
    python scripts\init_vault.py vault\
    echo ✓ Vault initialized
    echo.
)

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found
    echo    Copy .env.example to .env and configure your credentials
    echo    copy .env.example .env
    exit /b 1
)

REM Check if credentials.json exists
if not exist "credentials.json" (
    echo.
    echo ⚠️  Warning: credentials.json not found
    echo    Download Gmail API credentials from Google Cloud Console
    echo    and save as credentials.json
    echo.
    echo    Continuing without Gmail watcher...
    echo.
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Install Playwright browsers
echo 🌐 Installing Playwright browsers...
playwright install chromium
echo ✓ Playwright ready
echo.

REM Start system
echo 🚀 Starting AI Employee system...
echo.
echo Choose startup mode:
echo 1) Development (manual terminals)
echo 2) Production (PM2)
echo 3) Watchdog (single process)
echo.
set /p mode="Select mode (1-3): "

if "%mode%"=="1" (
    echo.
    echo Starting in development mode...
    echo.
    echo Open separate terminals and run:
    echo   Terminal 1: python src\orchestrator.py vault\
    echo   Terminal 2: python src\watchers\gmail_watcher.py vault\ credentials.json
    echo   Terminal 3: python src\watchers\filesystem_watcher.py vault\ vault\Drop\
    echo.
    pause
) else if "%mode%"=="2" (
    echo.
    echo Starting with PM2...
    where pm2 >nul 2>nul
    if errorlevel 1 (
        echo Installing PM2...
        npm install -g pm2
    )
    pm2 start ecosystem.config.js
    pm2 save
    echo.
    echo ✓ System started with PM2
    echo.
    echo Useful commands:
    echo   pm2 status       - Check process status
    echo   pm2 logs         - View logs
    echo   pm2 stop all     - Stop all processes
    echo   pm2 restart all  - Restart all processes
    echo.
    pause
) else if "%mode%"=="3" (
    echo.
    echo Starting watchdog...
    python src\watchdog.py vault\
) else (
    echo Invalid selection
    exit /b 1
)

echo.
echo ✅ AI Employee is ready!
echo.
echo Next steps:
echo 1. Open vault\Dashboard.md in Obsidian to monitor activity
echo 2. Drop files in vault\Drop\ to test file processing
echo 3. Review vault\Company_Handbook.md for behavior guidelines
echo.
echo 📚 Documentation: README.md
echo 🔧 Configuration: .env
echo 📊 Dashboard: vault\Dashboard.md
echo.
pause
