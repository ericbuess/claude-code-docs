#!/bin/bash
#
# Auto-sync script for Claude Code Documentation
# Safely pulls latest documentation updates from the GitHub repository
#
# Usage: ./auto-sync.sh [--quiet]
#

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$SCRIPT_DIR/sync.log"
LOCK_FILE="$SCRIPT_DIR/.sync.lock"
QUIET_MODE=false
MAX_LOG_SIZE=10485760  # 10MB

# Parse arguments
if [[ "${1:-}" == "--quiet" ]]; then
    QUIET_MODE=true
fi

# Logging function
log() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$message" >> "$LOG_FILE"
    if [[ "$QUIET_MODE" == "false" ]]; then
        echo "$message"
    fi
}

# Error handling
error_exit() {
    log "ERROR: $1"
    rm -f "$LOCK_FILE"
    exit 1
}

# Cleanup function
cleanup() {
    rm -f "$LOCK_FILE"
}

# Set up cleanup trap
trap cleanup EXIT

# Change to repository directory
cd "$REPO_DIR" || error_exit "Failed to change to repository directory: $REPO_DIR"

# Verify we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    error_exit "Not in a git repository: $REPO_DIR"
fi

# Check for lock file (prevent concurrent execution)
if [[ -f "$LOCK_FILE" ]]; then
    if [[ "$QUIET_MODE" == "false" ]]; then
        echo "Another sync process is already running (lock file exists). Exiting."
    fi
    exit 0
fi

# Create lock file
touch "$LOCK_FILE"

# Rotate log if needed
if [[ -f "$LOG_FILE" ]] && [[ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0) -gt $MAX_LOG_SIZE ]]; then
    mv "$LOG_FILE" "$LOG_FILE.old"
    log "Log rotated due to size limit"
fi

log "Starting auto-sync check for Claude Code docs..."

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
    error_exit "Could not determine default branch"
fi

log "Using branch: $DEFAULT_BRANCH"

# Fetch latest changes from remote without merging
log "Fetching latest changes from remote..."
if ! git fetch origin "$DEFAULT_BRANCH" --quiet; then
    error_exit "Failed to fetch from remote repository"
fi

# Check if local is behind remote
LOCAL_HASH=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse "origin/$DEFAULT_BRANCH")

if [[ "$LOCAL_HASH" == "$REMOTE_HASH" ]]; then
    log "Already up to date. No changes to pull."
    exit 0
fi

# Count commits behind
COMMITS_BEHIND=$(git rev-list "HEAD..origin/$DEFAULT_BRANCH" --count)
log "Local repository is $COMMITS_BEHIND commit(s) behind remote."

# Check for local changes that might conflict
if ! git diff-index --quiet HEAD --; then
    error_exit "Local changes detected. Please commit or stash changes before auto-sync."
fi

# Check which files will be updated
log "Files that will be updated:"
git diff --name-only HEAD "origin/$DEFAULT_BRANCH" | while read -r file; do
    log "  - $file"
done

# Pull the latest changes
log "Pulling latest changes..."
if ! git pull origin "$DEFAULT_BRANCH" --quiet; then
    error_exit "Failed to pull changes. Manual intervention may be required."
fi

# Log what was updated
NEW_HASH=$(git rev-parse HEAD)
log "Successfully updated from $LOCAL_HASH to $NEW_HASH"

# Show summary of documentation changes
if [[ -d "docs" ]]; then
    DOC_CHANGES=$(git diff --name-only "$LOCAL_HASH" "$NEW_HASH" -- docs/*.md 2>/dev/null | wc -l | tr -d ' ') || DOC_CHANGES=0
    if [[ "$DOC_CHANGES" -gt 0 ]]; then
        log "Updated $DOC_CHANGES documentation file(s):"
        git diff --name-only "$LOCAL_HASH" "$NEW_HASH" -- docs/*.md | while read -r file; do
            log "  - $(basename "$file")"
        done
    fi
else
    log "Note: docs/ directory not found, skipping documentation change summary"
fi

log "Auto-sync completed successfully!"