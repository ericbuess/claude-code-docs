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
QUIET_MODE=false

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
    exit 1
}

# Change to repository directory
cd "$REPO_DIR" || error_exit "Failed to change to repository directory: $REPO_DIR"

# Verify we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    error_exit "Not in a git repository: $REPO_DIR"
fi

log "Starting auto-sync check for Claude Code docs..."

# Fetch latest changes from remote without merging
log "Fetching latest changes from remote..."
if ! git fetch origin main --quiet; then
    error_exit "Failed to fetch from remote repository"
fi

# Check if local is behind remote
LOCAL_HASH=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse origin/main)

if [[ "$LOCAL_HASH" == "$REMOTE_HASH" ]]; then
    log "Already up to date. No changes to pull."
    exit 0
fi

# Count commits behind
COMMITS_BEHIND=$(git rev-list HEAD..origin/main --count)
log "Local repository is $COMMITS_BEHIND commit(s) behind remote."

# Check for local changes that might conflict
if ! git diff-index --quiet HEAD --; then
    error_exit "Local changes detected. Please commit or stash changes before auto-sync."
fi

# Check which files will be updated
log "Files that will be updated:"
git diff --name-only HEAD origin/main | while read -r file; do
    log "  - $file"
done

# Pull the latest changes
log "Pulling latest changes..."
if ! git pull origin main --quiet; then
    error_exit "Failed to pull changes. Manual intervention may be required."
fi

# Log what was updated
NEW_HASH=$(git rev-parse HEAD)
log "Successfully updated from $LOCAL_HASH to $NEW_HASH"

# Show summary of documentation changes
DOC_CHANGES=$(git diff --name-only "$LOCAL_HASH" "$NEW_HASH" -- docs/*.md | wc -l | tr -d ' ')
if [[ "$DOC_CHANGES" -gt 0 ]]; then
    log "Updated $DOC_CHANGES documentation file(s):"
    git diff --name-only "$LOCAL_HASH" "$NEW_HASH" -- docs/*.md | while read -r file; do
        log "  - $(basename "$file")"
    done
fi

log "Auto-sync completed successfully!"