#!/bin/bash
# Quick start script for Personal AI Employee
# Run this after initial setup to start all components

set -e

echo "🤖 Personal AI Employee - Quick Start"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Check if vault exists
if [ ! -d "vault" ]; then
    echo ""
    echo "📁 Initializing vault structure..."
    python scripts/init_vault.py vault/
    echo "✓ Vault initialized"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Warning: .env file not found"
    echo "   Copy .env.example to .env and configure your credentials"
    echo "   cp .env.example .env"
    exit 1
fi

# Check if credentials.json exists
if [ ! -f "credentials.json" ]; then
    echo ""
    echo "⚠️  Warning: credentials.json not found"
    echo "   Download Gmail API credentials from Google Cloud Console"
    echo "   and save as credentials.json"
    echo ""
    echo "   Continuing without Gmail watcher..."
fi

# Install dependencies
echo ""
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium --quiet
echo "✓ Playwright ready"

# Start system
echo ""
echo "🚀 Starting AI Employee system..."
echo ""
echo "Choose startup mode:"
echo "1) Development (manual terminals)"
echo "2) Production (PM2)"
echo "3) Watchdog (single process)"
echo ""
read -p "Select mode (1-3): " mode

case $mode in
    1)
        echo ""
        echo "Starting in development mode..."
        echo ""
        echo "Open separate terminals and run:"
        echo "  Terminal 1: python src/orchestrator.py vault/"
        echo "  Terminal 2: python src/watchers/gmail_watcher.py vault/ credentials.json"
        echo "  Terminal 3: python src/watchers/filesystem_watcher.py vault/ vault/Drop/"
        ;;
    2)
        echo ""
        echo "Starting with PM2..."
        if ! command -v pm2 &> /dev/null; then
            echo "Installing PM2..."
            npm install -g pm2
        fi
        pm2 start ecosystem.config.js
        pm2 save
        echo ""
        echo "✓ System started with PM2"
        echo ""
        echo "Useful commands:"
        echo "  pm2 status       - Check process status"
        echo "  pm2 logs         - View logs"
        echo "  pm2 stop all     - Stop all processes"
        echo "  pm2 restart all  - Restart all processes"
        ;;
    3)
        echo ""
        echo "Starting watchdog..."
        python src/watchdog.py vault/
        ;;
    *)
        echo "Invalid selection"
        exit 1
        ;;
esac

echo ""
echo "✅ AI Employee is ready!"
echo ""
echo "Next steps:"
echo "1. Open vault/Dashboard.md in Obsidian to monitor activity"
echo "2. Drop files in vault/Drop/ to test file processing"
echo "3. Review vault/Company_Handbook.md for behavior guidelines"
echo ""
echo "📚 Documentation: README.md"
echo "🔧 Configuration: .env"
echo "📊 Dashboard: vault/Dashboard.md"
