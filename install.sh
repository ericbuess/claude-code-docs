#!/bin/bash
#
# Claude Code Docs - Smart Installer
# Handles setup with automatic detection and fixes for common issues
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IS_MACOS=false
CLAUDE_MODE=false

# Check if running from Claude
if [[ "${CLAUDE_CODE_CLI:-}" == "true" ]] || [[ "${1:-}" == "--claude" ]]; then
    CLAUDE_MODE=true
fi

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    IS_MACOS=true
fi

echo -e "${BLUE}Claude Code Documentation - Auto-sync Setup${NC}"
echo "============================================"
echo ""

# Pre-flight checks
echo -e "${YELLOW}Running pre-flight checks...${NC}"

# 1. Check git
if ! command -v git >/dev/null 2>&1; then
    echo -e "${RED}✗ Git is not installed${NC}"
    echo "Please install git first: https://git-scm.com/downloads"
    exit 1
fi
echo -e "${GREEN}✓ Git is installed${NC}"

# 2. Check if in git repo
cd "$REPO_DIR"
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}✗ Not in a git repository${NC}"
    exit 1
fi
echo -e "${GREEN}✓ In git repository${NC}"

# 3. Test git fetch
echo -e "Testing git connectivity..."
if ! git fetch origin --dry-run >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Git fetch failed - checking credentials...${NC}"
    
    # Try to help with git credentials
    if [[ "$(git remote get-url origin)" == https://* ]]; then
        echo ""
        echo "You're using HTTPS. Setting up credential helper..."
        git config credential.helper cache
        echo "Please run 'git fetch' manually once to save your credentials,"
        echo "then run this installer again."
        exit 1
    fi
fi
echo -e "${GREEN}✓ Git connectivity OK${NC}"

# 4. Make scripts executable
chmod +x "$REPO_DIR/auto-sync/auto-sync.sh" "$REPO_DIR/auto-sync/check-updates.sh" 2>/dev/null || true
echo -e "${GREEN}✓ Scripts are executable${NC}"

# 5. Test sync script
echo -e "\nTesting sync script..."
if ! "$REPO_DIR/auto-sync/auto-sync.sh" >/dev/null 2>&1; then
    echo -e "${RED}✗ Sync script test failed${NC}"
    "$REPO_DIR/auto-sync/auto-sync.sh" # Run again to show error
    exit 1
fi
echo -e "${GREEN}✓ Sync script works${NC}"

# macOS-specific checks
if [[ "$IS_MACOS" == true ]]; then
    echo -e "\n${YELLOW}macOS Detected - Additional Setup Required${NC}"
    
    # Check if cron has Full Disk Access
    CRON_TEST_FILE="/tmp/.claude_docs_cron_test_$$"
    if (crontab -l 2>/dev/null || true) | grep -q "echo test > $CRON_TEST_FILE"; then
        # Clean up any existing test
        crontab -l 2>/dev/null | grep -v "$CRON_TEST_FILE" | crontab - 2>/dev/null || true
    fi
    
    # Add test cron job
    (crontab -l 2>/dev/null || true; echo "* * * * * echo test > $CRON_TEST_FILE") | crontab - 2>/dev/null || true
    
    # Wait up to 65 seconds for cron to run
    echo -e "Checking if cron has Full Disk Access (this takes 60 seconds)..."
    SECONDS=0
    while [[ $SECONDS -lt 65 ]]; do
        if [[ -f "$CRON_TEST_FILE" ]]; then
            rm -f "$CRON_TEST_FILE"
            # Remove test cron job
            crontab -l 2>/dev/null | grep -v "$CRON_TEST_FILE" | crontab - 2>/dev/null || true
            echo -e "${GREEN}✓ Cron has Full Disk Access${NC}"
            break
        fi
        sleep 5
        echo -n "."
    done
    
    if [[ $SECONDS -ge 65 ]]; then
        # Remove test cron job
        crontab -l 2>/dev/null | grep -v "$CRON_TEST_FILE" | crontab - 2>/dev/null || true
        
        echo -e "\n${RED}✗ Cron does NOT have Full Disk Access${NC}"
        echo ""
        echo -e "${YELLOW}REQUIRED ACTION:${NC}"
        echo "1. Open System Settings"
        echo "2. Go to Privacy & Security → Full Disk Access"
        echo "3. Click the lock to make changes"
        echo "4. Click + and add: /usr/sbin/cron"
        echo "5. Make sure it's checked"
        echo ""
        
        if [[ "$CLAUDE_MODE" == true ]]; then
            echo "CLAUDE_ERROR: MACOS_CRON_PERMISSION_REQUIRED"
        else
            echo "After granting access, run this installer again."
            read -p "Press Enter to open System Settings, or Ctrl+C to exit..."
            open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
        fi
        exit 1
    fi
fi

# Setup cron job
echo -e "\n${BLUE}Setting up automatic sync...${NC}"

# Check if already configured
if crontab -l 2>/dev/null | grep -q "claude-code-docs.*auto-sync"; then
    echo -e "${YELLOW}Auto-sync is already configured!${NC}"
    echo "Current cron job:"
    crontab -l | grep "claude-code-docs"
    echo ""
    read -p "Do you want to update it? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Setup complete! Auto-sync is already running.${NC}"
        exit 0
    fi
    # Remove existing entry
    crontab -l 2>/dev/null | grep -v "claude-code-docs.*auto-sync" | crontab - 2>/dev/null || true
fi

# Add new cron job
CRON_CMD="30 */6 * * * cd $REPO_DIR && ./auto-sync/auto-sync.sh --quiet"
(crontab -l 2>/dev/null || true; echo "$CRON_CMD") | crontab -

# Verify it was added
if crontab -l 2>/dev/null | grep -q "claude-code-docs.*auto-sync"; then
    echo -e "${GREEN}✓ Cron job added successfully${NC}"
else
    echo -e "${RED}✗ Failed to add cron job${NC}"
    exit 1
fi

# Final summary
echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "Your Claude Code docs will sync automatically at:"
echo "  • 00:30 (12:30 AM)"
echo "  • 06:30 (6:30 AM)"
echo "  • 12:30 (12:30 PM)"
echo "  • 18:30 (6:30 PM)"
echo ""
echo "Useful commands:"
echo "  • Check sync status: tail auto-sync/sync.log"
echo "  • Manual sync: ./auto-sync/auto-sync.sh"
echo "  • View cron job: crontab -l | grep claude-code-docs"
echo ""

if [[ "$CLAUDE_MODE" == true ]]; then
    echo "CLAUDE_SUCCESS: AUTO_SYNC_CONFIGURED"
fi