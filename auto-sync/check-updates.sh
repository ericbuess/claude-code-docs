#!/bin/bash
#
# Check if Claude Code Documentation has updates available
# Returns exit code 0 if updates available, 1 if up to date
#
# Usage: ./check-updates.sh [--verbose]
#

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
VERBOSE=false

# Parse arguments
if [[ "${1:-}" == "--verbose" ]]; then
    VERBOSE=true
fi

# Change to repository directory
cd "$REPO_DIR" || exit 2

# Verify we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "ERROR: Not in a git repository: $REPO_DIR" >&2
    exit 2
fi

# Fetch latest changes from remote without merging
if ! git fetch origin main --quiet 2>/dev/null; then
    echo "ERROR: Failed to fetch from remote repository" >&2
    exit 2
fi

# Check if local is behind remote
LOCAL_HASH=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse origin/main)

if [[ "$LOCAL_HASH" == "$REMOTE_HASH" ]]; then
    if [[ "$VERBOSE" == "true" ]]; then
        echo "Already up to date. No updates available."
    fi
    exit 1
fi

# Updates are available
COMMITS_BEHIND=$(git rev-list HEAD..origin/main --count)
DOC_CHANGES=$(git diff --name-only HEAD origin/main -- docs/*.md | wc -l | tr -d ' ')

if [[ "$VERBOSE" == "true" ]]; then
    echo "Updates available: $COMMITS_BEHIND commit(s) behind"
    echo "Documentation files changed: $DOC_CHANGES"
    
    if [[ "$DOC_CHANGES" -gt 0 ]]; then
        echo "Changed documentation files:"
        git diff --name-only HEAD origin/main -- docs/*.md | while read -r file; do
            echo "  - $(basename "$file")"
        done
    fi
else
    echo "$COMMITS_BEHIND"
fi

exit 0