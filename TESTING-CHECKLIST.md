# Claude Code Docs Windows Port - Testing Checklist

## Prerequisites Check
- [ ] Windows 10 or Windows 11 installed
- [ ] PowerShell 5.1 or higher (check with `$PSVersionTable.PSVersion`)
- [ ] Git for Windows installed (check with `git --version`)
- [ ] Claude Code installed and working

## Installation Testing

### Test 1: Batch File Installation
1. [ ] Double-click `install.bat`
2. [ ] Verify no error messages appear
3. [ ] Check that `%USERPROFILE%\.claude-code-docs` directory was created
4. [ ] Verify git repository was cloned successfully
5. [ ] Check that docs folder contains `.md` files

### Test 2: PowerShell Installation
1. [ ] Open PowerShell
2. [ ] Run: `powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1`
3. [ ] Verify installation completes without errors
4. [ ] Check for success message

### Test 3: Installation File Verification
After installation, verify these files exist:
- [ ] `%USERPROFILE%\.claude-code-docs\claude-docs-helper.ps1`
- [ ] `%USERPROFILE%\.claude-code-docs\Install-ClaudeCodeDocs.ps1`
- [ ] `%USERPROFILE%\.claude-code-docs\Uninstall-ClaudeCodeDocs.ps1`
- [ ] `%USERPROFILE%\.claude-code-docs\docs\*.md` (multiple documentation files)
- [ ] `%USERPROFILE%\.claude\commands\docs.md`

### Test 4: Settings.json Hook Verification
1. [ ] Open `%USERPROFILE%\.claude\settings.json`
2. [ ] Verify it contains a PreToolUse hook for claude-code-docs
3. [ ] Check that the hook command points to the PowerShell helper script

## Claude Code Integration Testing

### Test 5: Basic Command Functionality
Restart Claude Code, then test:
1. [ ] `/docs` - Should list all available documentation topics
2. [ ] `/docs hooks` - Should display hooks documentation
3. [ ] `/docs mcp` - Should display MCP documentation
4. [ ] `/docs memory` - Should display memory documentation

### Test 6: Freshness Check
1. [ ] `/docs -t` - Should show sync status with GitHub
2. [ ] `/docs -t hooks` - Should check status then show hooks docs
3. [ ] `/docs --check` - Should work same as -t flag

### Test 7: What's New Feature
1. [ ] `/docs whats new` - Should show recent documentation changes
2. [ ] `/docs what's new` - Alternative spelling should work
3. [ ] Verify commit links are displayed

### Test 8: Search Functionality
1. [ ] `/docs nonexistent` - Should show search results/suggestions
2. [ ] `/docs environment variables` - Should suggest relevant topics

### Test 9: Uninstall Instructions
1. [ ] `/docs uninstall` - Should display uninstall instructions
2. [ ] Verify instructions are Windows-specific (PowerShell commands)

## Update Testing

### Test 10: Auto-Update Hook
1. [ ] Make a change to a doc file in `%USERPROFILE%\.claude-code-docs\docs\`
2. [ ] Use `/docs` command
3. [ ] Verify it detects local changes
4. [ ] Run `git pull` manually to restore clean state

### Test 11: Manual Update Check
1. [ ] `/docs -t` to check current status
2. [ ] Verify it shows if you're up-to-date or behind

## Uninstallation Testing

### Test 12: Uninstall via Command
1. [ ] Run `/docs uninstall` in Claude Code
2. [ ] Follow the displayed PowerShell command
3. [ ] Verify uninstallation completes

### Test 13: Batch File Uninstallation
1. [ ] Reinstall first if needed
2. [ ] Double-click `uninstall.bat`
3. [ ] Confirm when prompted
4. [ ] Verify uninstallation completes

### Test 14: Uninstall Verification
After uninstallation, verify these are removed:
- [ ] `%USERPROFILE%\.claude-code-docs` directory
- [ ] `%USERPROFILE%\.claude\commands\docs.md` file
- [ ] Hooks removed from `%USERPROFILE%\.claude\settings.json`

## Edge Cases

### Test 15: Reinstallation
1. [ ] Install the tool
2. [ ] Run installer again without uninstalling
3. [ ] Verify it detects existing installation and updates

### Test 16: Migration from Old Location
1. [ ] Manually create a dummy installation at a different location
2. [ ] Run installer
3. [ ] Verify it detects and offers to migrate

### Test 17: Execution Policy Issues
1. [ ] Set strict execution policy: `Set-ExecutionPolicy Restricted`
2. [ ] Try running installer
3. [ ] Verify batch file still works with `-ExecutionPolicy Bypass`
4. [ ] Reset policy: `Set-ExecutionPolicy RemoteSigned`

### Test 18: No Git Installed
1. [ ] Temporarily rename git.exe to simulate missing git
2. [ ] Run installer
3. [ ] Verify it shows appropriate error message
4. [ ] Restore git.exe

### Test 19: Offline Mode
1. [ ] Disconnect from internet
2. [ ] Run `/docs hooks` 
3. [ ] Verify it works with cached docs
4. [ ] Run `/docs -t`
5. [ ] Verify it shows offline warning

### Test 20: Special Characters in Username
1. [ ] Test with Windows usernames containing spaces
2. [ ] Test with usernames containing special characters
3. [ ] Verify paths are properly quoted

## Performance Testing

### Test 21: Response Time
1. [ ] Measure time for `/docs` to list topics (should be < 1 second)
2. [ ] Measure time for `/docs hooks` to display (should be < 2 seconds)
3. [ ] Measure time for `/docs -t` sync check (should be < 5 seconds)

### Test 22: Large Documentation
1. [ ] Test with the largest documentation file
2. [ ] Verify it displays without truncation
3. [ ] Check memory usage remains reasonable

## Error Handling

### Test 23: Corrupted Installation
1. [ ] Delete random files from installation
2. [ ] Run various /docs commands
3. [ ] Verify graceful error messages
4. [ ] Run installer to repair

### Test 24: Permission Issues
1. [ ] Set read-only on installation directory
2. [ ] Try to update
3. [ ] Verify appropriate error message
4. [ ] Remove read-only attribute

## Final Verification

### Test 25: Complete Workflow
1. [ ] Fresh install via batch file
2. [ ] Use various /docs commands
3. [ ] Check for updates
4. [ ] Read multiple documents
5. [ ] Uninstall via batch file
6. [ ] Verify complete removal

## Sign-off

- [ ] All critical tests passed
- [ ] All edge cases handled appropriately
- [ ] Performance is acceptable
- [ ] Error messages are helpful
- [ ] Documentation is clear

**Tested by:** _________________
**Date:** _________________
**Windows Version:** _________________
**PowerShell Version:** _________________
**Issues Found:** _________________