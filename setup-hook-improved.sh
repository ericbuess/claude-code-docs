#!/bin/bash
set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SETTINGS_FILE="$HOME/.claude/settings.json"
TEMP_FILE="$SETTINGS_FILE.tmp.$$"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Cleanup function
cleanup() {
    rm -f "$TEMP_FILE"
}
trap cleanup EXIT

check_prerequisites() {
    if ! command -v jq &> /dev/null; then
        log_error "jq is not installed. Please install jq to use auto-update hooks."
        log_info "On macOS: brew install jq"
        log_info "On Ubuntu/Debian: sudo apt-get install jq"
        exit 1
    fi
}

validate_json() {
    local file="$1"
    if ! jq empty "$file" 2>/dev/null; then
        log_error "Invalid JSON in $file"
        return 1
    fi
    return 0
}

create_hook_command() {
    local script_dir="$1"
    # Escape the path for use in JSON and shell
    local escaped_dir=$(printf '%s' "$script_dir" | sed 's/[[\.*^$()+?{|]/\\&/g')
    
    cat << EOF
if [[ \$(jq -r .tool_input.file_path 2>/dev/null) == *${escaped_dir}/* ]]; then cd ${script_dir} && git pull --quiet; fi
EOF
}

update_existing_settings() {
    local script_dir="$1"
    local hook_command=$(create_hook_command "$script_dir")
    
    log_info "Updating existing settings.json..."
    
    # Create a backup
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup" || {
        log_error "Failed to create backup of settings.json"
        exit 1
    }
    
    # Build the jq filter to update settings
    jq --arg path "$script_dir" --arg cmd "$hook_command" '
        # Ensure hooks object exists
        .hooks = (.hooks // {}) |
        # Ensure PreToolUse array exists
        .hooks.PreToolUse = (.hooks.PreToolUse // []) |
        # Remove any existing Read matchers for this path
        .hooks.PreToolUse = [.hooks.PreToolUse[] | select(
            .matcher != "Read" or 
            (.hooks[]?.command // "" | contains($path) | not)
        )] |
        # Add our new hook
        .hooks.PreToolUse += [{
            "matcher": "Read",
            "hooks": [{
                "type": "command",
                "command": $cmd
            }]
        }]
    ' "$SETTINGS_FILE" > "$TEMP_FILE"
    
    # Validate the result
    if ! validate_json "$TEMP_FILE"; then
        log_error "Failed to create valid JSON"
        log_info "Restoring backup..."
        mv "$SETTINGS_FILE.backup" "$SETTINGS_FILE"
        exit 1
    fi
    
    # Apply the changes
    mv "$TEMP_FILE" "$SETTINGS_FILE"
    rm -f "$SETTINGS_FILE.backup"
    
    log_info "Settings updated successfully"
}

create_new_settings() {
    local script_dir="$1"
    local hook_command=$(create_hook_command "$script_dir")
    
    log_info "Creating new settings.json..."
    
    # Ensure .claude directory exists
    mkdir -p "$(dirname "$SETTINGS_FILE")"
    
    # Create new settings file
    cat > "$TEMP_FILE" << EOF
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "$hook_command"
          }
        ]
      }
    ]
  }
}
EOF
    
    # Validate and move
    if validate_json "$TEMP_FILE"; then
        mv "$TEMP_FILE" "$SETTINGS_FILE"
        log_info "Settings file created successfully"
    else
        log_error "Failed to create valid settings file"
        exit 1
    fi
}

verify_hook_installation() {
    local script_dir="$1"
    
    # Check if our hook is in the settings
    if jq -e --arg path "$script_dir" '
        .hooks.PreToolUse[]? | 
        select(.matcher == "Read") | 
        .hooks[]? | 
        select(.command | contains($path))
    ' "$SETTINGS_FILE" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

main() {
    log_info "Claude Code Docs Auto-Update Hook Setup"
    
    # Check prerequisites
    check_prerequisites
    
    # Check if this is being run from the correct directory
    if [ ! -f "$SCRIPT_DIR/docs/docs_manifest.json" ] && [ ! -d "$SCRIPT_DIR/docs" ]; then
        log_warn "This script should be run from the claude-code-docs directory"
        log_warn "Current directory: $SCRIPT_DIR"
    fi
    
    # Update or create settings
    if [ -f "$SETTINGS_FILE" ]; then
        # Validate existing settings
        if ! validate_json "$SETTINGS_FILE"; then
            log_error "Existing settings.json is invalid"
            log_info "Please fix or remove $SETTINGS_FILE and try again"
            exit 1
        fi
        update_existing_settings "$SCRIPT_DIR"
    else
        create_new_settings "$SCRIPT_DIR"
    fi
    
    # Verify installation
    if verify_hook_installation "$SCRIPT_DIR"; then
        log_info "${GREEN}✅ Auto-update hook installed successfully!${NC}"
        echo
        echo "Claude will now automatically run 'git pull' before reading docs from:"
        echo "  $SCRIPT_DIR"
        echo
        echo "To test: /user:docs hooks"
    else
        log_error "Hook installation could not be verified"
        log_info "Please check $SETTINGS_FILE manually"
        exit 1
    fi
}

# Run main function
main "$@"