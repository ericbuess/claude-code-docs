#!/bin/bash
#
# Diagnostic script for Claude Code Docs
# Helps identify common setup issues
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Claude Code Docs - Diagnostics${NC}"
echo "=============================="
echo ""

ISSUES_FOUND=0

# 1. Check git
echo -n "Git installed: "
if command -v git >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ (required)${NC}"
    ((ISSUES_FOUND++))
fi

# 2. Check repo
echo -n "In git repository: "
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    ((ISSUES_FOUND++))
fi

# 3. Check remote
echo -n "Git remote configured: "
if git remote get-url origin >/dev/null 2>&1; then
    REMOTE=$(git remote get-url origin)
    echo -e "${GREEN}✓${NC} ($REMOTE)"
else
    echo -e "${RED}✗${NC}"
    ((ISSUES_FOUND++))
fi

# 4. Check connectivity
echo -n "Git connectivity: "
if git ls-remote origin >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ (check credentials)${NC}"
    ((ISSUES_FOUND++))
fi

# 5. Check scripts
echo -n "Scripts executable: "
if [[ -x "auto-sync/auto-sync.sh" ]]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    chmod +x auto-sync/*.sh
    echo "  Fixed: made scripts executable"
fi

# 6. Check cron
echo -n "Auto-sync configured: "
if crontab -l 2>/dev/null | grep -q "claude-code-docs.*auto-sync"; then
    echo -e "${GREEN}✓${NC}"
    CRON_PATH=$(crontab -l | grep "claude-code-docs" | sed 's/.*cd \([^ ]*\) &&.*/\1/')
    echo "  Syncing from: $CRON_PATH"
else
    echo -e "${YELLOW}Not configured${NC}"
    echo "  Run ./install.sh to set up"
fi

# 7. macOS specific
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "\n${BLUE}macOS Specific Checks:${NC}"
    
    echo -n "Cron Full Disk Access: "
    # Quick test
    TEST_FILE="/tmp/.claude_docs_diag_$$"
    if echo "* * * * * touch $TEST_FILE" | crontab - 2>/dev/null; then
        sleep 61
        if [[ -f "$TEST_FILE" ]]; then
            rm -f "$TEST_FILE"
            echo -e "${GREEN}✓${NC}"
        else
            echo -e "${RED}✗${NC}"
            echo "  Required: System Settings → Privacy & Security → Full Disk Access → Add /usr/sbin/cron"
            ((ISSUES_FOUND++))
        fi
        # Clean up test cron
        crontab -l 2>/dev/null | grep -v "$TEST_FILE" | crontab - 2>/dev/null || true
    else
        echo -e "${YELLOW}Unable to test${NC}"
    fi
fi

# 8. Check logs
echo -e "\n${BLUE}Recent Sync Activity:${NC}"
if [[ -f "auto-sync/sync.log" ]]; then
    echo "Last 3 sync attempts:"
    grep -E "(Starting|completed|ERROR)" auto-sync/sync.log | tail -3 | sed 's/^/  /'
else
    echo "  No sync log found (auto-sync hasn't run yet)"
fi

# Summary
echo ""
if [[ $ISSUES_FOUND -eq 0 ]]; then
    echo -e "${GREEN}✅ Everything looks good!${NC}"
else
    echo -e "${RED}Found $ISSUES_FOUND issue(s)${NC}"
    echo "Run ./install.sh to fix most issues automatically"
fi