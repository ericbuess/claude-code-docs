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

# Detect the default branch
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
if [[ -z "$DEFAULT_BRANCH" ]]; then
    # Fallback to common branch names
    for branch in main master; do
        if git show-ref --verify --quiet "refs/remotes/origin/$branch"; then
            DEFAULT_BRANCH="$branch"
            break
        fi
    done
fi

if [[ -z "$DEFAULT_BRANCH" ]]; then
    echo "ERROR: Could not determine default branch" >&2
    exit 2
fi

# Fetch latest changes from remote without merging
if ! git fetch origin "$DEFAULT_BRANCH" --quiet 2>/dev/null; then
    echo "ERROR: Failed to fetch from remote repository" >&2
    exit 2
fi

# Check if local is behind remote
LOCAL_HASH=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse "origin/$DEFAULT_BRANCH")

if [[ "$LOCAL_HASH" == "$REMOTE_HASH" ]]; then
    if [[ "$VERBOSE" == "true" ]]; then
        echo "Already up to date. No updates available."
    fi
    exit 1
fi

# Updates are available
COMMITS_BEHIND=$(git rev-list "HEAD..origin/$DEFAULT_BRANCH" --count)
DOC_CHANGES=$(git diff --name-only HEAD "origin/$DEFAULT_BRANCH" -- docs/*.md 2>/dev/null | wc -l | tr -d ' ') || DOC_CHANGES=0

if [[ "$VERBOSE" == "true" ]]; then
    echo "Updates available: $COMMITS_BEHIND commit(s) behind"
    echo "Documentation files changed: $DOC_CHANGES"
    
    if [[ "$DOC_CHANGES" -gt 0 ]]; then
        echo "Changed documentation files:"
        git diff --name-only HEAD "origin/$DEFAULT_BRANCH" -- docs/*.md 2>/dev/null | while read -r file; do
            echo "  - $(basename "$file")"
        done
    fi
else
    echo "$COMMITS_BEHIND"
fi

exit 0