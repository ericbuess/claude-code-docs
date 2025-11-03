#!/bin/bash
set -euo pipefail

# Claude Code Documentation Enhanced Helper Script
# This script extends the standard template with enhanced features
# Installation path: ~/.claude-code-docs/scripts/claude-docs-helper.sh

# Script version
ENHANCED_VERSION="0.4.0"

# Fixed installation path
DOCS_PATH="$HOME/.claude-code-docs"
SCRIPTS_PATH="$DOCS_PATH/scripts"

# Source the standard template for base functionality
TEMPLATE_PATH="$SCRIPTS_PATH/claude-docs-helper.sh.template"
if [[ -f "$TEMPLATE_PATH" ]]; then
    # Define a function to run template commands
    run_template_command() {
        bash "$TEMPLATE_PATH" "$@"
    }
else
    echo "❌ Error: Standard template not found at $TEMPLATE_PATH"
    echo "   Please reinstall: curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash"
    exit 1
fi

# Check if Python is available and version is 3.12+
check_python() {
    if ! command -v python3 &> /dev/null; then
        return 1
    fi

    local python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
    local python_major=$(echo "$python_version" | cut -d. -f1)
    local python_minor=$(echo "$python_version" | cut -d. -f2)

    if [[ "$python_major" -ge 3 && "$python_minor" -ge 12 ]]; then
        return 0
    else
        return 1
    fi
}

# Check if enhanced features are available
check_enhanced_available() {
    # Check Python version
    if ! check_python; then
        return 1
    fi

    # Check if lookup_paths.py exists
    if [[ ! -f "$SCRIPTS_PATH/lookup_paths.py" ]]; then
        return 1
    fi

    # Check if paths_manifest.json exists with enhanced paths
    if [[ ! -f "$DOCS_PATH/paths_manifest.json" ]]; then
        return 1
    fi

    local path_count=$(python3 -c "import json; data=json.load(open('$DOCS_PATH/paths_manifest.json')); print(data['metadata'].get('total_paths', 0))" 2>/dev/null || echo "0")

    # Enhanced manifest has 449+ paths (standard has 47)
    if [[ "$path_count" -ge 100 ]]; then
        return 0
    else
        return 1
    fi
}

# Enhanced search - uses lookup_paths.py for fuzzy path search
enhanced_search() {
    if ! check_enhanced_available; then
        echo "❌ Enhanced search not available"
        echo "   Requires: Python 3.12+, lookup_paths.py, enhanced manifest"
        echo "   Reinstall with enhanced features: curl -fsSL .../install.sh | bash"
        echo ""
        echo "Falling back to standard search..."
        echo ""
        run_template_command "$@"
        return
    fi

    local query="$*"
    echo "🔍 Searching 449 paths for: $query"
    echo ""

    if python3 "$SCRIPTS_PATH/lookup_paths.py" "$query" 2>/dev/null; then
        echo ""
        echo "💡 Tip: Use '/docs <topic>' to read a specific document"
    else
        echo "⚠️  Search failed"
        echo "Falling back to standard search..."
        echo ""
        run_template_command "$@"
    fi
}

# Full-text content search
search_content() {
    if ! check_enhanced_available; then
        echo "❌ Content search not available"
        echo "   Requires: Python 3.12+, search index, enhanced features"
        echo "   Install with: curl -fsSL .../install.sh | bash"
        echo ""
        return 1
    fi

    local query="$*"
    echo "📖 Searching documentation content for: $query"
    echo ""

    if python3 "$SCRIPTS_PATH/lookup_paths.py" --search-content "$query" 2>/dev/null; then
        echo ""
        echo "💡 Tip: Use '/docs <topic>' to read the full document"
    else
        echo "⚠️  Content search failed"
        echo "   Try: cd $DOCS_PATH && grep -ri '$query' docs/"
    fi
}

# Validate all paths
validate_paths() {
    if ! check_enhanced_available; then
        echo "❌ Path validation not available"
        echo "   Requires: Python 3.12+, lookup_paths.py"
        echo ""
        return 1
    fi

    echo "🔍 Validating all documentation paths..."
    echo "This may take 30-60 seconds..."
    echo ""

    if python3 "$SCRIPTS_PATH/lookup_paths.py" --validate-all 2>/dev/null; then
        echo ""
        echo "✅ Validation complete"
    else
        echo "⚠️  Validation failed"
        echo "   Check your internet connection"
    fi
}

# Update all documentation (fetch all 449+ docs)
update_all_docs() {
    if ! check_enhanced_available; then
        echo "❌ Enhanced update not available"
        echo "   Requires: Python 3.12+, main.py"
        echo ""
        echo "Falling back to standard git pull..."
        cd "$DOCS_PATH" && git pull
        return
    fi

    echo "🔄 Updating all documentation (449+ paths)..."
    echo "This may take 5-10 minutes..."
    echo ""

    if python3 "$SCRIPTS_PATH/main.py" --update-all 2>/dev/null; then
        echo ""
        echo "✅ Documentation updated successfully"

        # Rebuild search index if available
        if [[ -f "$SCRIPTS_PATH/build_search_index.py" ]]; then
            echo "Rebuilding search index..."
            python3 "$SCRIPTS_PATH/build_search_index.py" >/dev/null 2>&1 || true
        fi
    else
        echo "⚠️  Enhanced update failed"
        echo "Falling back to git pull..."
        cd "$DOCS_PATH" && git pull
    fi
}

# Show enhanced help
show_enhanced_help() {
    run_template_command --help 2>/dev/null || run_template_command
    echo ""
    echo "─────────────────────────────────────────────────────────────────"
    echo "Enhanced Edition Commands (requires Python 3.12+):"
    echo "─────────────────────────────────────────────────────────────────"
    echo ""
    echo "Search & Discovery:"
    echo "  --search <query>        Fuzzy search 449 paths"
    echo "  --search-content <term> Full-text content search"
    echo ""
    echo "Maintenance:"
    echo "  --validate              Validate all paths (check for 404s)"
    echo "  --update-all            Fetch all 449 documentation pages"
    echo ""
    echo "Status:"
    echo "  --version               Show version information"
    echo "  --status                Show installation status"
    echo ""

    if check_enhanced_available; then
        echo "✅ Enhanced features: AVAILABLE"
    else
        echo "❌ Enhanced features: NOT AVAILABLE"
        if ! check_python; then
            echo "   Missing: Python 3.12+"
        else
            echo "   Missing: Enhanced installation files"
        fi
        echo "   Install: curl -fsSL .../install.sh | bash (answer Y)"
    fi
    echo ""
}

# Show version information
show_version() {
    echo "Claude Code Docs - Enhanced Edition v$ENHANCED_VERSION"
    echo ""
    echo "Components:"
    echo "  • Helper script: v$ENHANCED_VERSION"

    if [[ -f "$TEMPLATE_PATH" ]]; then
        local template_version=$(grep "SCRIPT_VERSION=" "$TEMPLATE_PATH" | head -1 | cut -d'"' -f2)
        echo "  • Template: v$template_version"
    fi

    if check_python; then
        local python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
        echo "  • Python: $python_version ✓"
    else
        echo "  • Python: Not available"
    fi

    echo ""
    echo "Features:"
    if check_enhanced_available; then
        local path_count=$(python3 -c "import json; data=json.load(open('$DOCS_PATH/paths_manifest.json')); print(data['metadata'].get('total_paths', 0))" 2>/dev/null || echo "unknown")
        echo "  ✅ Enhanced features: ENABLED"
        echo "  ✅ Documentation paths: $path_count"
        echo "  ✅ Fuzzy search: Available"
        echo "  ✅ Content search: Available"
        echo "  ✅ Path validation: Available"
    else
        echo "  ❌ Enhanced features: DISABLED"
        echo "     (Standard 47 docs available)"
    fi
    echo ""
}

# Show installation status
show_status() {
    echo "Installation Status"
    echo "───────────────────"
    echo ""
    echo "Location: $DOCS_PATH"

    if [[ -d "$DOCS_PATH" ]]; then
        echo "Status: ✅ Installed"
    else
        echo "Status: ❌ Not found"
        return 1
    fi

    echo ""
    echo "Standard Features:"
    [[ -f "$TEMPLATE_PATH" ]] && echo "  ✅ Template script" || echo "  ❌ Template script"
    [[ -f "$DOCS_PATH/claude-docs-helper.sh" ]] && echo "  ✅ Helper script" || echo "  ❌ Helper script"
    [[ -d "$DOCS_PATH/docs" ]] && echo "  ✅ Documentation directory" || echo "  ❌ Documentation directory"

    local doc_count=$(find "$DOCS_PATH/docs" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    echo "  📄 Documentation files: $doc_count"

    echo ""
    echo "Enhanced Features:"

    if check_python; then
        local python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
        echo "  ✅ Python $python_version"
    else
        echo "  ❌ Python 3.12+ (not available)"
    fi

    [[ -f "$SCRIPTS_PATH/lookup_paths.py" ]] && echo "  ✅ lookup_paths.py" || echo "  ❌ lookup_paths.py"
    [[ -f "$SCRIPTS_PATH/main.py" ]] && echo "  ✅ main.py" || echo "  ❌ main.py"
    [[ -f "$DOCS_PATH/paths_manifest.json" ]] && echo "  ✅ paths_manifest.json" || echo "  ❌ paths_manifest.json"

    if [[ -f "$DOCS_PATH/paths_manifest.json" ]]; then
        local path_count=$(python3 -c "import json; data=json.load(open('$DOCS_PATH/paths_manifest.json')); print(data['metadata'].get('total_paths', 0))" 2>/dev/null || echo "unknown")
        echo "  📊 Manifest paths: $path_count"
    fi

    echo ""
    if check_enhanced_available; then
        echo "Overall: ✅ Enhanced features AVAILABLE"
    else
        echo "Overall: ⚠️  Standard features only"
        echo ""
        echo "To enable enhanced features:"
        echo "  curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash"
        echo "  (Answer 'y' to install enhanced features)"
    fi
    echo ""
}

# Main command handling
case "${1:-}" in
    --search)
        shift
        enhanced_search "$@"
        ;;
    --search-content)
        shift
        search_content "$@"
        ;;
    --validate)
        validate_paths
        ;;
    --update-all)
        update_all_docs
        ;;
    --help|-h)
        show_enhanced_help
        ;;
    --version)
        show_version
        ;;
    --status)
        show_status
        ;;
    *)
        # Delegate all other commands to standard template
        run_template_command "$@"
        ;;
esac

# Ensure script always exits successfully
exit 0
