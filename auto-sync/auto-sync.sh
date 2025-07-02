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
    # Cleanup will be handled by the trap
    exit 1
}

# Cleanup function
cleanup() {
    # Only remove lock file if not using flock
    if ! command -v flock >/dev/null 2>&1; then
        rm -f "$LOCK_FILE"
    fi
}

# Set up cleanup trap
trap cleanup EXIT

# Change to repository directory
cd "$REPO_DIR" || error_exit "Failed to change to repository directory: $REPO_DIR"

# Verify we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    error_exit "Not in a git repository: $REPO_DIR"
fi

# Use flock for better lock handling if available
if command -v flock >/dev/null 2>&1; then
    # Try to acquire lock with flock
    exec 200>"$LOCK_FILE"
    if ! flock -n 200; then
        if [[ "$QUIET_MODE" == "false" ]]; then
            echo "Another sync process is already running (could not acquire lock). Exiting."
        fi
        exit 0
    fi
    # Lock acquired, no need to manually remove lock file as it will be released on exit
else
    # Fallback to traditional lock file with improved atomicity
    if ! (set -C; echo $$ > "$LOCK_FILE") 2>/dev/null; then
        if [[ "$QUIET_MODE" == "false" ]]; then
            # Check if the process that created the lock is still running
            if [[ -f "$LOCK_FILE" ]]; then
                OLD_PID=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
                if [[ -n "$OLD_PID" ]] && kill -0 "$OLD_PID" 2>/dev/null; then
                    echo "Another sync process is already running (PID: $OLD_PID). Exiting."
                else
                    # Stale lock file, remove it
                    log "Removing stale lock file from PID $OLD_PID"
                    rm -f "$LOCK_FILE"
                    # Try again
                    if ! (set -C; echo $$ > "$LOCK_FILE") 2>/dev/null; then
                        echo "Failed to acquire lock after removing stale lock. Exiting."
                        exit 1
                    fi
                fi
            else
                echo "Another sync process is already running. Exiting."
                exit 0
            fi
        else
            exit 0
        fi
    fi
fi

# Rotate log if needed
if [[ -f "$LOG_FILE" ]] && [[ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0) -gt $MAX_LOG_SIZE ]]; then
    mv "$LOG_FILE" "$LOG_FILE.old"
    log "Log rotated due to size limit"
fi

log "Starting auto-sync check for Claude Code docs..."

# macOS cron permission check
if [[ "$OSTYPE" == "darwin"* ]] && [[ -n "${TERM_PROGRAM:-}" ]]; then
    # We're on macOS and running from a terminal (not cron)
    # Skip the check - user is running manually
    :
elif [[ "$OSTYPE" == "darwin"* ]] && [[ -z "${TERM_PROGRAM:-}" ]]; then
    # We're on macOS and likely running from cron
    # Quick test to see if we can write to a test location
    TEST_FILE="/tmp/.claude_docs_cron_test_$$"
    if ! touch "$TEST_FILE" 2>/dev/null; then
        error_exit "macOS cron lacks Full Disk Access. See auto-sync/README.md for setup instructions."
    fi
    rm -f "$TEST_FILE"
fi

# Detect the default branch
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
if [[ -z "$DEFAULT_BRANCH" ]]; then
    log "Remote HEAD not set. Setting it now..."
    # Try to set the remote HEAD automatically
    if git remote set-head origin -a >/dev/null 2>&1; then
        DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
        log "Remote HEAD set to: $DEFAULT_BRANCH"
    else
        # Fallback to common branch names
        for branch in main master; do
            if git show-ref --verify --quiet "refs/remotes/origin/$branch"; then
                DEFAULT_BRANCH="$branch"
                log "Using detected branch: $DEFAULT_BRANCH"
                break
            fi
        done
    fi
fi

if [[ -z "$DEFAULT_BRANCH" ]]; then
    error_exit "Could not determine default branch. Please run: git remote set-head origin -a"
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