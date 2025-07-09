#!/bin/bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/ericbuess/claude-code-docs.git"
CLAUDE_DIR="$HOME/.claude"
COMMANDS_DIR="$CLAUDE_DIR/commands"

# Helper functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

check_prerequisites() {
    local missing_deps=()
    
    # Check for required commands
    for cmd in git jq; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies and try again."
        exit 1
    fi
}

ensure_claude_directory() {
    if [ ! -d "$CLAUDE_DIR" ]; then
        log_warn "Claude directory not found at $CLAUDE_DIR"
        log_info "Creating Claude directory..."
        mkdir -p "$CLAUDE_DIR" || {
            log_error "Failed to create Claude directory"
            exit 1
        }
    fi
    
    # Ensure commands directory exists
    mkdir -p "$COMMANDS_DIR" || {
        log_error "Failed to create commands directory"
        exit 1
    }
}

clone_or_update_repo() {
    local target_dir="claude-code-docs"
    
    if [ -d "$target_dir" ]; then
        log_info "Repository already exists. Updating..."
        cd "$target_dir" || exit 1
        
        # Store current state
        local current_branch=$(git branch --show-current 2>/dev/null || echo "")
        local has_changes=$(git status --porcelain)
        
        if [ -n "$has_changes" ]; then
            log_warn "Local changes detected. Skipping update."
        else
            git pull --quiet || {
                log_error "Failed to update repository"
                exit 1
            }
            log_info "Repository updated successfully"
        fi
    else
        log_info "Cloning repository..."
        git clone --quiet "$REPO_URL" "$target_dir" || {
            log_error "Failed to clone repository"
            exit 1
        }
        cd "$target_dir" || exit 1
        log_info "Repository cloned successfully"
    fi
    
    # Return absolute path
    pwd
}

create_docs_command() {
    local docs_path="$1"
    local command_file="$COMMANDS_DIR/docs.md"
    
    log_info "Creating /user:docs command..."
    
    # Create command with proper escaping
    cat > "$command_file" << EOF
${docs_path}/ contains a local update copy of all docs for Claude Code and is faster for you to access. Please use a Read task to research Claude Code docs there (rather than a web fetch) and tell me about the following: \$ARGUMENTS
EOF
    
    if [ -f "$command_file" ]; then
        log_info "Command created successfully"
    else
        log_error "Failed to create command file"
        exit 1
    fi
}

setup_auto_update_hook() {
    local docs_path="$1"
    
    log_info "Setting up auto-update hook..."
    
    # Check if setup-hook.sh exists
    if [ ! -f "setup-hook.sh" ]; then
        log_error "setup-hook.sh not found in repository"
        exit 1
    fi
    
    # Run hook setup
    bash setup-hook.sh || {
        log_error "Hook setup failed"
        log_warn "You can still use the docs, but auto-updates won't work"
        log_warn "Try running 'bash setup-hook.sh' manually later"
        return 1
    }
    
    return 0
}

validate_installation() {
    local docs_path="$1"
    local errors=0
    
    log_info "Validating installation..."
    
    # Check if docs directory exists and has content
    if [ ! -d "$docs_path/docs" ] || [ -z "$(ls -A "$docs_path/docs" 2>/dev/null)" ]; then
        log_error "Docs directory is empty or missing"
        ((errors++))
    fi
    
    # Check if command was created
    if [ ! -f "$COMMANDS_DIR/docs.md" ]; then
        log_error "Command file was not created"
        ((errors++))
    fi
    
    # Check if manifest exists
    if [ ! -f "$docs_path/docs/docs_manifest.json" ]; then
        log_warn "Documentation manifest not found - docs may need updating"
    fi
    
    return $errors
}

main() {
    log_info "Claude Code Docs Installer v2.0"
    echo
    
    # Check prerequisites
    check_prerequisites
    
    # Ensure Claude directory structure exists
    ensure_claude_directory
    
    # Store starting directory
    local start_dir=$(pwd)
    
    # Clone or update repository
    local docs_path=$(clone_or_update_repo)
    
    # Create docs command
    create_docs_command "$docs_path"
    
    # Setup auto-update hook
    setup_auto_update_hook "$docs_path"
    local hook_status=$?
    
    # Return to starting directory
    cd "$start_dir" || exit 1
    
    # Validate installation
    validate_installation "$docs_path"
    local validation_status=$?
    
    echo
    if [ $validation_status -eq 0 ] && [ $hook_status -eq 0 ]; then
        log_info "${GREEN}Installation completed successfully!${NC}"
    elif [ $validation_status -eq 0 ]; then
        log_warn "Installation completed with warnings"
    else
        log_error "Installation completed with errors"
    fi
    
    echo
    echo "📍 Docs location: $docs_path"
    echo "🔧 Command: /user:docs"
    echo "📚 Example: /user:docs hooks"
    
    if [ $hook_status -ne 0 ]; then
        echo
        log_warn "Auto-updates are not configured. Run 'cd $docs_path && bash setup-hook.sh' to enable."
    fi
}

# Run main function
main "$@"