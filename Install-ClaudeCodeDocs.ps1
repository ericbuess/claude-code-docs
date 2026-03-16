# Claude Code Docs Installer for Windows v0.3.3
# PowerShell port of the original bash installer
# This script installs/migrates claude-code-docs to $env:USERPROFILE\.claude-code-docs

param(
    [switch]$Force = $false,
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$Script:Version = "0.3.3-windows"

Write-Host "Claude Code Docs Installer for Windows v$($Script:Version)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Fixed installation location
$INSTALL_DIR = Join-Path $env:USERPROFILE ".claude-code-docs"

# Detect OS type
Write-Host "[OK] Detected Windows" -ForegroundColor Green

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow

# Check for git
try {
    $null = git --version 2>&1
    Write-Host "  [OK] git found" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] git is required but not installed" -ForegroundColor Red
    Write-Host "Please install git from https://git-scm.com/download/win and try again" -ForegroundColor Yellow
    exit 1
}

# Check for PowerShell version (need 5.1 or higher for JSON support)
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-Host "[ERROR] PowerShell 5.1 or higher is required" -ForegroundColor Red
    Write-Host "Please update PowerShell and try again" -ForegroundColor Yellow
    exit 1
}
Write-Host "  [OK] PowerShell $($PSVersionTable.PSVersion) found" -ForegroundColor Green

Write-Host "[OK] All dependencies satisfied" -ForegroundColor Green

# Function to find existing installations from configs
function Find-ExistingInstallations {
    $paths = @()
    
    # Check command file for paths
    $commandFile = Join-Path $env:USERPROFILE ".claude\commands\docs.md"
    if (Test-Path $commandFile) {
        $content = Get-Content $commandFile -Raw
        
        # Look for paths in various formats
        $matches = [regex]::Matches($content, 'Execute:\s*([^\s"]+claude-code-docs[^\s"]*)')
        foreach ($match in $matches) {
            $path = $match.Groups[1].Value
            $path = $path.Replace('~', $env:USERPROFILE)
            $path = $path.Replace('/', '\')
            
            # Extract directory part
            if (Test-Path $path -PathType Container) {
                $paths += $path
            } elseif ($path -match '\\claude-docs-helper\.(ps1|sh)$') {
                $dir = Split-Path $path -Parent
                if ((Test-Path $dir -PathType Container) -and ((Split-Path $dir -Leaf) -eq "claude-code-docs")) {
                    $paths += $dir
                }
            }
        }
        
        # Also check for LOCAL DOCS AT format (v0.1)
        $matches = [regex]::Matches($content, 'LOCAL DOCS AT:\s*([^\s]+)/docs/')
        foreach ($match in $matches) {
            $path = $match.Groups[1].Value
            $path = $path.Replace('~', $env:USERPROFILE)
            $path = $path.Replace('/', '\')
            if (Test-Path $path -PathType Container) {
                $paths += $path
            }
        }
    }
    
    # Check settings.json hooks for paths
    $settingsFile = Join-Path $env:USERPROFILE ".claude\settings.json"
    if (Test-Path $settingsFile) {
        try {
            $settings = Get-Content $settingsFile -Raw | ConvertFrom-Json
            $hooks = $settings.hooks.PreToolUse.hooks.command
            
            foreach ($cmd in $hooks) {
                if ($cmd -match 'claude-code-docs') {
                    # Extract paths
                    $matches = [regex]::Matches($cmd, '[^\s"]*claude-code-docs[^\s"]*')
                    foreach ($match in $matches) {
                        $path = $match.Value
                        $path = $path.Replace('~', $env:USERPROFILE)
                        $path = $path.Replace('/', '\')
                        
                        # Clean up path to get the claude-code-docs directory
                        if ($path -match '(.+\\claude-code-docs)(\\.*)?$') {
                            $path = $Matches[1]
                            if (Test-Path $path -PathType Container) {
                                $paths += $path
                            }
                        }
                    }
                }
            }
        } catch {
            # Ignore JSON parsing errors
        }
    }
    
    # Also check current directory if running from an installation
    $currentPath = Get-Location
    $manifestPath = Join-Path $currentPath "docs\docs_manifest.json"
    if ((Test-Path $manifestPath) -and ($currentPath.Path -ne $INSTALL_DIR)) {
        $paths += $currentPath.Path
    }
    
    # Deduplicate and exclude new location
    $paths | Where-Object { $_ -ne $INSTALL_DIR } | Select-Object -Unique
}

# Function to migrate from old location
function Migrate-Installation {
    param($OldDir)
    
    Write-Host "[INFO] Found existing installation at: $OldDir" -ForegroundColor Yellow
    Write-Host "   Migrating to: $INSTALL_DIR" -ForegroundColor Yellow
    Write-Host ""
    
    # Check if old dir has uncommitted changes
    $shouldPreserve = $false
    if (Test-Path (Join-Path $OldDir ".git")) {
        Push-Location $OldDir
        try {
            $status = git status --porcelain 2>$null
            if ($status) {
                $shouldPreserve = $true
                Write-Host "[WARNING] Uncommitted changes detected in old installation" -ForegroundColor Yellow
            }
        } finally {
            Pop-Location
        }
    }
    
    # Fresh install at new location
    Write-Host "Installing fresh at $env:USERPROFILE\.claude-code-docs..." -ForegroundColor Yellow
    git clone -b $Branch https://github.com/ericbuess/claude-code-docs.git $INSTALL_DIR
    Set-Location $INSTALL_DIR
    
    # Remove old directory if safe
    if (-not $shouldPreserve) {
        Write-Host "Removing old installation..." -ForegroundColor Yellow
        Remove-Item -Path $OldDir -Recurse -Force
        Write-Host "[OK] Old installation removed" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "[INFO] Old installation preserved at: $OldDir" -ForegroundColor Cyan
        Write-Host "   (has uncommitted changes)" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "[SUCCESS] Migration complete!" -ForegroundColor Green
}

# Function to safely update git repository
function Update-GitRepository {
    param($RepoDir)
    
    Set-Location $RepoDir
    
    # Get current branch
    $currentBranch = git rev-parse --abbrev-ref HEAD 2>$null
    if (-not $currentBranch) { $currentBranch = "unknown" }
    
    $targetBranch = $Branch
    
    if ($currentBranch -ne $targetBranch) {
        Write-Host "  Switching from $currentBranch to $targetBranch branch..." -ForegroundColor Yellow
    } else {
        Write-Host "  Updating $targetBranch branch..." -ForegroundColor Yellow
    }
    
    # Set git config for pull strategy if not set
    $pullRebase = git config pull.rebase 2>$null
    if (-not $pullRebase) {
        git config pull.rebase false
    }
    
    Write-Host "Updating to latest version..." -ForegroundColor Yellow
    
    # Try regular pull first
    try {
        git pull --quiet origin $targetBranch 2>$null
        return $true
    } catch {
        Write-Host "  Standard update failed, trying harder..." -ForegroundColor Yellow
    }
    
    # Fetch latest
    try {
        git fetch origin $targetBranch 2>$null
    } catch {
        Write-Host "  [WARNING] Could not fetch from GitHub (offline?)" -ForegroundColor Yellow
        return $false
    }
    
    # Check for changes
    $hasConflicts = $false
    $hasLocalChanges = $false
    $needsConfirmation = $false
    
    if ($currentBranch -ne $targetBranch) {
        Write-Host "  Branch switch detected, forcing clean state..." -ForegroundColor Yellow
        $needsConfirmation = $false
    } else {
        # Check for conflicts and changes
        $status = git status --porcelain
        $nonManifestChanges = $status | Where-Object { $_ -notmatch "docs[/\\]docs_manifest\.json" }
        
        if ($nonManifestChanges) {
            $hasLocalChanges = $true
            $needsConfirmation = $true
        }
    }
    
    # If we have significant changes, ask user for confirmation
    if ($needsConfirmation -and -not $Force) {
        Write-Host ""
        Write-Host "[WARNING] Local changes detected in your installation:" -ForegroundColor Yellow
        if ($hasLocalChanges) {
            Write-Host "  * Modified files (other than docs_manifest.json)" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "The installer will reset to a clean state, discarding these changes." -ForegroundColor Yellow
        Write-Host "Note: Changes to docs_manifest.json are handled automatically." -ForegroundColor Yellow
        Write-Host ""
        
        $response = Read-Host "Continue and discard local changes? [y/N]"
        if ($response -ne 'y' -and $response -ne 'Y') {
            Write-Host "Installation cancelled. Your local changes are preserved." -ForegroundColor Yellow
            Write-Host "To proceed later, either:" -ForegroundColor Cyan
            Write-Host "  1. Manually resolve the issues, or" -ForegroundColor Cyan
            Write-Host "  2. Run the installer again with -Force flag" -ForegroundColor Cyan
            return $false
        }
        Write-Host "  Proceeding with clean installation..." -ForegroundColor Yellow
    }
    
    # Force clean state
    Write-Host "  Updating to clean state..." -ForegroundColor Yellow
    
    # Abort any in-progress merge/rebase
    git merge --abort 2>$null | Out-Null
    git rebase --abort 2>$null | Out-Null
    
    # Force checkout target branch
    git checkout -B $targetBranch "origin/$targetBranch" 2>$null | Out-Null
    
    # Reset to clean state
    git reset --hard "origin/$targetBranch" 2>$null | Out-Null
    
    # Clean any untracked files
    git clean -fd 2>$null | Out-Null
    
    Write-Host "  [OK] Updated successfully to clean state" -ForegroundColor Green
    
    return $true
}

# Function to cleanup old installations
function Remove-OldInstallations {
    param($OldInstalls)
    
    if ($OldInstalls.Count -eq 0) {
        return
    }
    
    Write-Host ""
    Write-Host "Cleaning up old installations..." -ForegroundColor Yellow
    Write-Host "Found $($OldInstalls.Count) old installation(s) to remove:" -ForegroundColor Yellow
    
    foreach ($oldDir in $OldInstalls) {
        if (-not $oldDir) { continue }
        
        Write-Host "  - $oldDir" -ForegroundColor Cyan
        
        # Check if it has uncommitted changes
        if (Test-Path (Join-Path $oldDir ".git")) {
            Push-Location $oldDir
            try {
                $status = git status --porcelain 2>$null
                if (-not $status) {
                    Pop-Location
                    Remove-Item -Path $oldDir -Recurse -Force
                    Write-Host "    [OK] Removed (clean)" -ForegroundColor Green
                } else {
                    Pop-Location
                    Write-Host "    [WARNING] Preserved (has uncommitted changes)" -ForegroundColor Yellow
                }
            } catch {
                Pop-Location
                Write-Host "    [WARNING] Preserved (error checking status)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "    [WARNING] Preserved (not a git repo)" -ForegroundColor Yellow
        }
    }
}

# Main installation logic
Write-Host ""

# Find old installations first (before any config changes)
Write-Host "Checking for existing installations..." -ForegroundColor Yellow
$existingInstalls = @(Find-ExistingInstallations)

if ($existingInstalls.Count -gt 0) {
    Write-Host "Found $($existingInstalls.Count) existing installation(s):" -ForegroundColor Yellow
    foreach ($install in $existingInstalls) {
        Write-Host "  - $install" -ForegroundColor Cyan
    }
    Write-Host ""
}

# Check if already installed at new location
if ((Test-Path $INSTALL_DIR) -and (Test-Path (Join-Path $INSTALL_DIR "docs\docs_manifest.json"))) {
    Write-Host "[OK] Found installation at $env:USERPROFILE\.claude-code-docs" -ForegroundColor Green
    Write-Host "  Updating to latest version..." -ForegroundColor Yellow
    
    # Update it safely
    Update-GitRepository -RepoDir $INSTALL_DIR
    Set-Location $INSTALL_DIR
} else {
    # Need to install at new location
    if ($existingInstalls.Count -gt 0) {
        # Migrate from old location
        Migrate-Installation -OldDir $existingInstalls[0]
    } else {
        # Fresh installation
        Write-Host "No existing installation found" -ForegroundColor Yellow
        Write-Host "Installing fresh to $env:USERPROFILE\.claude-code-docs..." -ForegroundColor Yellow
        
        git clone -b $Branch https://github.com/ericbuess/claude-code-docs.git $INSTALL_DIR
        Set-Location $INSTALL_DIR
    }
}

# Now we're in $INSTALL_DIR, set up the new script-based system
Write-Host ""
Write-Host "Setting up Claude Code Docs v$($Script:Version)..." -ForegroundColor Cyan

# Copy helper script from template (or create it)
Write-Host "Installing helper script..." -ForegroundColor Yellow
$helperScriptPath = Join-Path $INSTALL_DIR "claude-docs-helper.ps1"

# Check if we have the Windows helper script in the repo
if (-not (Test-Path $helperScriptPath)) {
    Write-Host "  [INFO] Helper script will be created on first use" -ForegroundColor Cyan
}

Write-Host "[OK] Helper script ready" -ForegroundColor Green

# Always update command (in case it points to old location)
Write-Host "Setting up /docs command..." -ForegroundColor Yellow
$commandsDir = Join-Path $env:USERPROFILE ".claude\commands"
if (-not (Test-Path $commandsDir)) {
    New-Item -ItemType Directory -Path $commandsDir -Force | Out-Null
}

# Create docs command for Windows
$commandContent = @'
Execute the Claude Code Docs helper script at ~/.claude-code-docs/claude-docs-helper.ps1

Usage:
- /docs - List all available documentation topics
- /docs <topic> - Read specific documentation with link to official docs
- /docs -t - Check sync status without reading a doc
- /docs -t <topic> - Check freshness then read documentation
- /docs whats new - Show recent documentation changes (or "what's new")

Examples of expected output:

When reading a doc:
COMMUNITY MIRROR: https://github.com/ericbuess/claude-code-docs
OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code

[Doc content here...]

Official page: https://docs.anthropic.com/en/docs/claude-code/hooks

When showing what's new:
Recent documentation updates:

* 5 hours ago:
  https://github.com/ericbuess/claude-code-docs/commit/eacd8e1
  data-usage: https://docs.anthropic.com/en/docs/claude-code/data-usage
     Added: Privacy safeguards
  security: https://docs.anthropic.com/en/docs/claude-code/security
     Data flow and dependencies section moved here

Full changelog: https://github.com/ericbuess/claude-code-docs/commits/main/docs
COMMUNITY MIRROR - NOT AFFILIATED WITH ANTHROPIC

Every request checks for the latest documentation from GitHub (takes ~0.4s).
The helper script handles all functionality including auto-updates.

'@

# Add Windows-specific execution command
$commandContent += "Execute: powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$($env:USERPROFILE)\.claude-code-docs\claude-docs-helper.ps1`" `$ARGUMENTS"

$commandFile = Join-Path $commandsDir "docs.md"
$commandContent | Out-File $commandFile -Encoding UTF8
Write-Host "[OK] Created /docs command" -ForegroundColor Green

# Always update hook
Write-Host "Setting up automatic updates..." -ForegroundColor Yellow

# Windows hook command
$hookCommand = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$($env:USERPROFILE)\.claude-code-docs\claude-docs-helper.ps1`" hook-check"

$settingsFile = Join-Path $env:USERPROFILE ".claude\settings.json"

if (Test-Path $settingsFile) {
    # Update existing settings.json
    Write-Host "  Updating Claude settings..." -ForegroundColor Yellow
    
    $settings = Get-Content $settingsFile -Raw | ConvertFrom-Json
    
    # Remove old hooks containing claude-code-docs
    if ($settings.hooks.PreToolUse) {
        $settings.hooks.PreToolUse = @($settings.hooks.PreToolUse | Where-Object {
            -not ($_.hooks[0].command -match "claude-code-docs")
        })
    }
    
    # Add our new hook
    if (-not $settings.hooks) {
        $settings | Add-Member -NotePropertyName "hooks" -NotePropertyValue @{} -Force
    }
    if (-not $settings.hooks.PreToolUse) {
        $settings.hooks | Add-Member -NotePropertyName "PreToolUse" -NotePropertyValue @() -Force
    }
    
    $newHook = @{
        matcher = "Read"
        hooks = @(
            @{
                type = "command"
                command = $hookCommand
            }
        )
    }
    
    $settings.hooks.PreToolUse += $newHook
    
    $settings | ConvertTo-Json -Depth 10 | Out-File $settingsFile -Encoding UTF8
    Write-Host "[OK] Updated Claude settings" -ForegroundColor Green
} else {
    # Create new settings.json
    Write-Host "  Creating Claude settings..." -ForegroundColor Yellow
    
    $settings = @{
        hooks = @{
            PreToolUse = @(
                @{
                    matcher = "Read"
                    hooks = @(
                        @{
                            type = "command"
                            command = $hookCommand
                        }
                    )
                }
            )
        }
    }
    
    $settings | ConvertTo-Json -Depth 10 | Out-File $settingsFile -Encoding UTF8
    Write-Host "[OK] Created Claude settings" -ForegroundColor Green
}

# Clean up old installations
Remove-OldInstallations -OldInstalls $existingInstalls

# Success message
Write-Host ""
Write-Host "[SUCCESS] Claude Code Docs for Windows v$($Script:Version) installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Command: /docs (user)" -ForegroundColor Cyan
Write-Host "Location: $($env:USERPROFILE)\.claude-code-docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage examples:" -ForegroundColor Yellow
Write-Host "  /docs hooks         # Read hooks documentation"
Write-Host "  /docs -t           # Check when docs were last updated"
Write-Host "  /docs what's new   # See recent documentation changes"
Write-Host ""
Write-Host "Auto-updates: Enabled - syncs automatically when GitHub has newer content" -ForegroundColor Green
Write-Host ""
Write-Host "Available topics:" -ForegroundColor Yellow
Get-ChildItem (Join-Path $INSTALL_DIR "docs") -Filter "*.md" -ErrorAction SilentlyContinue | 
    ForEach-Object { $_.BaseName } | 
    Sort-Object | 
    Format-Wide -Column 3
Write-Host ""
Write-Host "[NOTE] Restart Claude Code for auto-updates to take effect" -ForegroundColor Yellow