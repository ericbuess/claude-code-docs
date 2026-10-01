# Claude Code Docs for Windows

This is a Windows port of the claude-code-docs tool, allowing Windows users to access Claude Code documentation locally.

## 🪟 Windows Installation

### Prerequisites

- **Git for Windows**: Download from [git-scm.com](https://git-scm.com/download/win)
- **PowerShell**: Pre-installed on Windows 10/11
- **Claude Code**: Obviously :)

### Quick Install

Run this command in PowerShell:

```powershell
# Download and run the installer
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install-windows.ps1" -OutFile "$env:TEMP\install-claude-docs.ps1"; powershell -ExecutionPolicy Bypass -File "$env:TEMP\install-claude-docs.ps1"
```

Or manually:

1. Clone the repository:
```powershell
git clone https://github.com/ericbuess/claude-code-docs.git "$env:USERPROFILE\.claude-code-docs"
```

2. Run the Windows installer:
```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude-code-docs\install-windows.ps1"
```

## Usage

After installation and restarting Claude Code:

### List all documentation topics
```
/docs
```

### Read specific documentation
```
/docs settings
/docs mcp
/docs hooks
```

### Check for updates
```
/docs -t
```

## Files Created

The Windows installer creates:

1. **PowerShell Helper Script**: `~\.claude-code-docs\docs-helper.ps1`
   - Handles all /docs functionality
   - Reads markdown files from the docs folder
   - Supports update checking

2. **Command File**: `~\.claude\commands\docs.md`
   - Registers the /docs command in Claude Code
   - Points to the PowerShell helper script

## Differences from Linux/Mac Version

- Uses PowerShell instead of Bash
- Path uses `C:\Users\%USERNAME%` instead of `~`
- Command execution uses `powershell -ExecutionPolicy Bypass`
- No hook support (Windows doesn't support bash hooks)

## Troubleshooting

### PowerShell Execution Policy Error

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Git Not Found

Install Git for Windows from: https://git-scm.com/download/win

### /docs Command Not Working

1. Restart Claude Code after installation
2. Check if the command file exists:
```powershell
Test-Path "$env:USERPROFILE\.claude\commands\docs.md"
```

### Documentation Not Updating

Manually update:
```powershell
cd "$env:USERPROFILE\.claude-code-docs"
git pull origin main
```

## Uninstalling

To remove the Windows installation:

```powershell
# Remove installation directory
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude-code-docs"

# Remove command file
Remove-Item "$env:USERPROFILE\.claude\commands\docs.md"
```

## Contributing

This Windows port was created by the community. Improvements welcome!

## Credits

- Original claude-code-docs by [@ericbuess](https://github.com/ericbuess)
- Windows port by community contributors

## License

Same as the original project - see LICENSE file.