# Claude Code Documentation Mirror - Windows Edition

[![Platform](https://img.shields.io/badge/platform-Windows-blue)]()
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-blue)]()
[![Version](https://img.shields.io/badge/version-0.3.3--windows-green)]()

Windows port of the Claude Code documentation mirror tool. This provides local access to Claude Code documentation with automatic updates from the official GitHub repository.

## 🆕 Windows Port Features

This is a complete PowerShell port of the original bash/Unix tool, maintaining full compatibility with Claude Code on Windows:

- ✅ **Full Windows compatibility**: Native PowerShell scripts
- ✅ **Same functionality**: All features from the original tool
- ✅ **Easy installation**: Simple batch files or PowerShell commands
- ✅ **Automatic updates**: Syncs with the latest documentation
- ✅ **Claude Code integration**: Works seamlessly with `/docs` command

## Prerequisites

Required software:
- **Windows 10/11** (Windows 7/8 may work but untested)
- **PowerShell 5.1+** (comes with Windows 10/11)
- **Git for Windows** - [Download here](https://git-scm.com/download/win)
- **Claude Code** - Obviously :)

## Installation

### Method 1: Using Batch File (Easiest)

1. Download or clone this repository
2. Double-click `install.bat`
3. Follow the prompts

### Method 2: Using PowerShell

Open PowerShell as Administrator and run:

```powershell
# Navigate to the repository directory
cd C:\path\to\claude-code-docs

# Run the installer
powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1
```

### Method 3: Direct Download and Install

```powershell
# Download the installer
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/your-username/claude-code-docs/main/Install-ClaudeCodeDocs.ps1" -OutFile "Install-ClaudeCodeDocs.ps1"

# Run it
powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1

# Clean up
Remove-Item Install-ClaudeCodeDocs.ps1
```

## What Gets Installed

The installer will:
1. Install to `%USERPROFILE%\.claude-code-docs` (e.g., `C:\Users\YourName\.claude-code-docs`)
2. Create the `/docs` command in `%USERPROFILE%\.claude\commands\docs.md`
3. Set up auto-update hooks in `%USERPROFILE%\.claude\settings.json`
4. Clone the documentation repository with all docs

## Usage

After installation, restart Claude Code and use the `/docs` command:

### Basic Commands

```bash
/docs                    # List all available documentation topics
/docs hooks              # Read hooks documentation
/docs mcp                # Read MCP documentation
/docs memory             # Read memory documentation
/docs changelog          # Read Claude Code release notes
```

### Check for Updates

```bash
/docs -t                 # Check sync status with GitHub
/docs -t hooks          # Check status, then read hooks docs
```

### See What's New

```bash
/docs what's new        # Show recent documentation changes
/docs whats new         # Alternative spelling works too
```

### Uninstall

```bash
/docs uninstall         # Get uninstall instructions
```

## Troubleshooting

### PowerShell Execution Policy

If you get an execution policy error:

```powershell
# Option 1: Run with bypass (recommended)
powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1

# Option 2: Temporarily change policy (requires admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Git Not Found

If the installer says git is not found:
1. Install Git for Windows from https://git-scm.com/download/win
2. Restart your PowerShell/Command Prompt
3. Try the installation again

### Command Not Found

If `/docs` returns "command not found":
1. Check if the command file exists:
   ```powershell
   Test-Path "$env:USERPROFILE\.claude\commands\docs.md"
   ```
2. Restart Claude Code to reload commands
3. Re-run the installation script

### Documentation Not Updating

If documentation seems outdated:
1. Run `/docs -t` to check sync status
2. Manually update:
   ```powershell
   cd $env:USERPROFILE\.claude-code-docs
   git pull
   ```

### Permission Errors

If you get permission errors:
1. Make sure you're not running PowerShell as Administrator (unless necessary)
2. Check that you have write access to your user profile directory
3. Close any programs that might be using the files

## Uninstalling

### Method 1: Using the Command

In Claude Code:
```bash
/docs uninstall
```
Then follow the instructions provided.

### Method 2: Using Batch File

Double-click `uninstall.bat` in the installation directory.

### Method 3: Using PowerShell

```powershell
& "$env:USERPROFILE\.claude-code-docs\Uninstall-ClaudeCodeDocs.ps1"
```

### Method 4: Manual Uninstall

1. Delete the installation directory:
   ```powershell
   Remove-Item -Path "$env:USERPROFILE\.claude-code-docs" -Recurse -Force
   ```

2. Remove the command file:
   ```powershell
   Remove-Item -Path "$env:USERPROFILE\.claude\commands\docs.md" -Force
   ```

3. Remove hooks from settings.json (edit the file manually or use the uninstaller)

## File Structure

```
%USERPROFILE%\.claude-code-docs\
├── Install-ClaudeCodeDocs.ps1     # Main installer script
├── claude-docs-helper.ps1         # Helper script for /docs command
├── Uninstall-ClaudeCodeDocs.ps1   # Uninstaller script
├── install.bat                     # Batch wrapper for easy installation
├── uninstall.bat                   # Batch wrapper for easy uninstallation
├── docs\                           # Documentation files
│   ├── *.md                        # Individual documentation files
│   └── docs_manifest.json          # Documentation manifest
└── README-WINDOWS.md               # This file
```

## Differences from Unix Version

### Path Differences
- Unix: `~/.claude-code-docs`
- Windows: `%USERPROFILE%\.claude-code-docs`

### Script Extensions
- Unix: `.sh` scripts
- Windows: `.ps1` PowerShell scripts

### Command Execution
- Unix: Direct bash execution
- Windows: PowerShell with execution policy bypass

### JSON Handling
- Unix: Uses `jq` for JSON manipulation
- Windows: Uses PowerShell's `ConvertFrom-Json` and `ConvertTo-Json`

## Advanced Usage

### Force Update/Reinstall

```powershell
# Force installation even with local changes
powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1 -Force

# Use a different branch
powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1 -Branch dev
```

### Search Across All Docs

Using PowerShell:
```powershell
# Search for a term across all documentation
Get-ChildItem "$env:USERPROFILE\.claude-code-docs\docs" -Filter "*.md" | 
    Select-String "search term" | 
    Format-List -Property Filename, LineNumber, Line
```

### Check Git Status

```powershell
cd $env:USERPROFILE\.claude-code-docs
git status
git log --oneline -10
```

## Security Notes

- The installer modifies `%USERPROFILE%\.claude\settings.json` to add an auto-update hook
- Scripts run with `ExecutionPolicy Bypass` to avoid policy restrictions
- All operations are limited to your user profile directory
- No administrative privileges required
- No data is sent externally - everything is local

## Known Issues

- Auto-updates may occasionally fail on some network configurations
- PowerShell execution policy may need to be adjusted on some systems
- Line endings in documentation files use Unix format (LF) but display correctly

## Contributing

This is a Windows port of the original claude-code-docs tool. For issues specific to the Windows version, please note that in your bug reports.

## License

Documentation content belongs to Anthropic.
This Windows port is open source - contributions welcome!

## Credits

- Original tool: https://github.com/ericbuess/claude-code-docs
- Windows port maintains full compatibility with the original