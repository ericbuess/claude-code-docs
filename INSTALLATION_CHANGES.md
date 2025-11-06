# Installation Script Changes - Clean Install Strategy

## Summary

The install script has been updated to implement a **clean installation strategy** that ensures a fresh installation every time by removing any existing `~/.claude-code-docs` directory before proceeding.

## Changes Made

### 1. New Function: `check_and_remove_existing_install()`
**Location:** Lines 41-90

**Purpose:** Detects and removes any existing installation at `~/.claude-code-docs` before proceeding with fresh installation.

**Features:**
- Checks if `~/.claude-code-docs` directory exists
- Detects uncommitted changes in git repository
- Prompts user for confirmation before deletion
- Shows clear warnings if uncommitted changes will be lost
- Safely removes the directory

**User Experience:**
```bash
⚠️  Existing installation detected at: ~/.claude-code-docs

This installation will be completely removed to ensure a clean installation.

⚠️  WARNING: This directory has uncommitted changes!
   All local modifications will be lost.

Continue and delete existing installation? [y/N]:
```

### 2. Updated Main Installation Flow
**Location:** Lines 240-274

**New 3-Stage Process:**

**Stage 1: Remove Existing Installation**
```bash
# STAGE 1: Check and remove existing installation at fixed location
check_and_remove_existing_install
```

**Stage 2: Find Old Installations in Other Locations**
```bash
# STAGE 2: Find old installations from configs (for cleanup later)
echo "Checking for existing installations in other locations..."
```

**Stage 3: Fresh Installation**
```bash
# STAGE 3: Fresh installation at ~/.claude-code-docs
echo ""
echo "Installing to ~/.claude-code-docs..."
git clone -b "$INSTALL_BRANCH" https://github.com/costiash/claude-code-docs.git "$INSTALL_DIR"
cd "$INSTALL_DIR"
echo "✓ Repository cloned successfully"
```

### 3. Removed Unused Functions

**Removed:**
- `migrate_installation()` - No longer needed with clean install approach
- `safe_git_update()` - No longer needed with clean install approach

These functions handled complex migration and update scenarios that are no longer necessary since we always perform a fresh installation.

### 4. Updated Script Comments
**Location:** Lines 4-10

Added clear documentation of the installation strategy:
```bash
# Installation Strategy: Always perform a fresh installation at the fixed location
#   1. Remove any existing installation at ~/.claude-code-docs (with user confirmation)
#   2. Clone fresh from GitHub
#   3. Set up commands and hooks
#   4. Clean up any old installations in other locations
```

## Benefits

### 1. **Simplicity**
- Eliminates complex migration logic
- Reduces code complexity by ~150 lines
- Easier to maintain and debug

### 2. **Reliability**
- No merge conflicts or git state issues
- Every installation is guaranteed fresh
- Predictable and consistent behavior

### 3. **Safety**
- Checks for uncommitted changes before deletion
- Requires explicit user confirmation
- Clear warnings about data loss

### 4. **Clean State**
- No leftover files or configuration
- Fresh git repository every time
- Eliminates potential corruption issues

## User Impact

### Installation Behavior
**Before:**
- Attempted to update existing installation
- Complex merge and conflict resolution
- Could leave installation in broken state

**After:**
- Always performs fresh installation
- Prompts for confirmation if installation exists
- Guarantees clean, working state

### User Actions Required

**First-time users:** No change - installation proceeds normally

**Existing users:** Will be prompted:
```bash
⚠️  Existing installation detected at: ~/.claude-code-docs

This installation will be completely removed to ensure a clean installation.

Continue and delete existing installation? [y/N]:
```

**Users with uncommitted changes:** Will see additional warning:
```bash
⚠️  WARNING: This directory has uncommitted changes!
   All local modifications will be lost.
```

## Testing Recommendations

### Test Scenarios

1. **Fresh Installation** (no existing directory)
   ```bash
   # Should install without prompts
   ./install.sh
   ```

2. **Re-installation** (clean existing directory)
   ```bash
   # Should prompt for confirmation, then proceed
   ./install.sh
   ```

3. **Re-installation** (with uncommitted changes)
   ```bash
   # Should show warning about uncommitted changes
   cd ~/.claude-code-docs
   echo "test" > test.txt
   git add test.txt
   cd -
   ./install.sh
   ```

4. **User Cancellation**
   ```bash
   # Should exit cleanly when user answers 'N'
   ./install.sh  # Answer 'N' at prompt
   # Verify existing installation is preserved
   ls ~/.claude-code-docs
   ```

### Expected Outcomes

✅ **Fresh install:** Completes without prompts
✅ **Re-install (clean):** Prompts once, installs successfully
✅ **Re-install (dirty):** Shows uncommitted changes warning, prompts for confirmation
✅ **User cancels:** Exits cleanly, preserves existing installation
✅ **Script errors:** No syntax errors (`bash -n install.sh` passes)

## Migration Path

### From Previous Versions

Users upgrading from v0.3.3 or earlier will experience:

1. Detection of existing installation
2. Confirmation prompt
3. Complete removal of old installation
4. Fresh installation of v0.3.4
5. Cleanup of any old installations in other locations

**No manual intervention required** - the script handles everything automatically after user confirmation.

## Code Metrics

### Lines Changed
- **Added:** ~50 lines (new function + updated flow)
- **Removed:** ~150 lines (unused functions)
- **Net change:** -100 lines (20% reduction in script size)

### Complexity Reduction
- **Functions removed:** 2 (migrate_installation, safe_git_update)
- **Conditional branches reduced:** ~15
- **Git operations simplified:** From ~30 to ~5

## Rollback Plan

If issues arise, users can:

1. **Revert to previous installer:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/v0.3.3/install.sh | bash
   ```

2. **Manual cleanup:**
   ```bash
   rm -rf ~/.claude-code-docs
   rm -f ~/.claude/commands/docs.md
   # Edit ~/.claude/settings.json to remove hooks
   ```

3. **Fresh install from specific branch:**
   ```bash
   git clone -b <branch> https://github.com/costiash/claude-code-docs.git ~/.claude-code-docs
   cd ~/.claude-code-docs
   ./install.sh
   ```

## Future Improvements

Potential enhancements for future versions:

1. **Backup option:** Offer to backup existing installation before removal
2. **Selective cleanup:** Option to preserve certain files/directories
3. **Dry-run mode:** Show what would be removed without actually removing
4. **Silent mode:** Skip prompts with `--force` flag for CI/CD environments

## Conclusion

This update significantly simplifies the installation process while maintaining safety and reliability. The clean installation strategy eliminates complex edge cases and ensures users always get a working installation.

**Status:** ✅ Ready for testing and deployment
**Version:** 0.3.4
**Date:** 2025-11-06
