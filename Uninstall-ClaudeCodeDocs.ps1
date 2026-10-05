# Claude Code Documentation Mirror - Windows Uninstaller
# PowerShell port of the original bash uninstaller
# Dynamically finds and removes all installations

param(
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"

Write-Host "Claude Code Documentation Mirror - Uninstaller for Windows" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Function to find all installations from configs
function Find-AllInstallations {
    $paths = @()
    
    # From command file
    $commandFile = Join-Path $env:USERPROFILE ".claude\commands\docs.md"
    if (Test-Path $commandFile) {
        $content = Get-Content $commandFile -Raw
        
        # Look for paths in Execute commands
        $matches = [regex]::Matches($content, 'Execute:.*?([A-Za-z]:[^"]*claude-code-docs[^"]*)')
        foreach ($match in $matches) {
            $path = $match.Groups[1].Value
            $path = $path.Replace('~', $env:USERPROFILE)
            $path = $path.Replace('/', '\')
            
            # Extract directory part
            if ($path -match '\\claude-docs-helper\.(ps1|sh)$') {
                $dir = Split-Path $path -Parent
                if ((Test-Path $dir -PathType Container)) {
                    $paths += $dir
                }
            } elseif (Test-Path $path -PathType Container) {
                $paths += $path
            }
        }
        
        # Also check for powershell.exe commands
        $matches = [regex]::Matches($content, 'powershell\.exe.*?"([^"]*claude-code-docs[^"]*)"')
        foreach ($match in $matches) {
            $path = $match.Groups[1].Value
            $path = $path.Replace('$env:USERPROFILE', $env:USERPROFILE)
            
            if ($path -match '\\claude-docs-helper\.ps1$') {
                $dir = Split-Path $path -Parent
                if ((Test-Path $dir -PathType Container)) {
                    $paths += $dir
                }
            }
        }
    }
    
    # From hooks in settings.json
    $settingsFile = Join-Path $env:USERPROFILE ".claude\settings.json"
    if (Test-Path $settingsFile) {
        try {
            $settings = Get-Content $settingsFile -Raw | ConvertFrom-Json
            
            if ($settings.hooks.PreToolUse) {
                foreach ($hook in $settings.hooks.PreToolUse) {
                    if ($hook.hooks[0].command -match 'claude-code-docs') {
                        $cmd = $hook.hooks[0].command
                        
                        # Extract paths from various formats
                        $matches = [regex]::Matches($cmd, '[A-Za-z]:[^"]*claude-code-docs[^"]*')
                        foreach ($match in $matches) {
                            $path = $match.Value
                            $path = $path.Replace('$env:USERPROFILE', $env:USERPROFILE)
                            
                            # Clean up path to get the claude-code-docs directory
                            if ($path -match '(.+\\claude-code-docs)(\\.*)?$') {
                                $cleanPath = $Matches[1]
                                if (Test-Path $cleanPath -PathType Container) {
                                    $paths += $cleanPath
                                }
                            }
                        }
                        
                        # Also check for powershell.exe format
                        if ($cmd -match 'powershell\.exe.*?"([^"]*claude-code-docs[^"]*)"') {
                            $path = $Matches[1]
                            $path = $path.Replace('$env:USERPROFILE', $env:USERPROFILE)
                            
                            if ($path -match '\\claude-docs-helper\.ps1$') {
                                $dir = Split-Path $path -Parent
                                if ((Test-Path $dir -PathType Container)) {
                                    $paths += $dir
                                }
                            }
                        }
                    }
                }
            }
        } catch {
            Write-Host "  Warning: Could not parse settings.json" -ForegroundColor Yellow
        }
    }
    
    # Deduplicate
    $paths | Select-Object -Unique
}

# Main uninstall logic
$installations = @(Find-AllInstallations)

if ($installations.Count -gt 0) {
    Write-Host "Found installations at:" -ForegroundColor Yellow
    foreach ($path in $installations) {
        Write-Host "  📁 $path" -ForegroundColor Cyan
    }
    Write-Host ""
}

Write-Host "This will remove:" -ForegroundColor Yellow
Write-Host "  • The /docs command from $env:USERPROFILE\.claude\commands\docs.md"
Write-Host "  • All claude-code-docs hooks from $env:USERPROFILE\.claude\settings.json"
if ($installations.Count -gt 0) {
    Write-Host "  • Installation directories (if safe to remove)"
}
Write-Host ""

if (-not $Force) {
    $response = Read-Host "Continue? (y/N)"
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Remove command file
$commandFile = Join-Path $env:USERPROFILE ".claude\commands\docs.md"
if (Test-Path $commandFile) {
    Remove-Item $commandFile -Force
    Write-Host "✓ Removed /docs command" -ForegroundColor Green
}

# Remove hooks from settings.json
$settingsFile = Join-Path $env:USERPROFILE ".claude\settings.json"
if (Test-Path $settingsFile) {
    # Create backup
    $backupFile = "$settingsFile.backup"
    Copy-Item $settingsFile $backupFile -Force
    
    try {
        $settings = Get-Content $settingsFile -Raw | ConvertFrom-Json
        
        # Remove ALL hooks containing claude-code-docs
        if ($settings.hooks.PreToolUse) {
            $filteredHooks = @()
            foreach ($hook in $settings.hooks.PreToolUse) {
                if (-not ($hook.hooks[0].command -match "claude-code-docs")) {
                    $filteredHooks += $hook
                }
            }
            $settings.hooks.PreToolUse = $filteredHooks
            
            # Clean up empty structures
            if ($settings.hooks.PreToolUse.Count -eq 0) {
                $settings.hooks.PSObject.Properties.Remove('PreToolUse')
            }
            if (@($settings.hooks.PSObject.Properties).Count -eq 0) {
                $settings.PSObject.Properties.Remove('hooks')
            }
        }
        
        $settings | ConvertTo-Json -Depth 10 | Out-File $settingsFile -Encoding UTF8
        Write-Host "✓ Removed hooks (backup: $backupFile)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error updating settings.json: $_" -ForegroundColor Red
        Write-Host "  Manual removal may be required" -ForegroundColor Yellow
    }
}

# Remove directories
if ($installations.Count -gt 0) {
    Write-Host ""
    foreach ($path in $installations) {
        if (-not (Test-Path $path)) {
            continue
        }
        
        $gitDir = Join-Path $path ".git"
        if (Test-Path $gitDir) {
            # Save current directory
            $currentDir = Get-Location
            Set-Location $path
            
            try {
                $status = git status --porcelain 2>$null
                if (-not $status) {
                    Set-Location $currentDir
                    Remove-Item -Path $path -Recurse -Force
                    Write-Host "✓ Removed $path (clean git repo)" -ForegroundColor Green
                } else {
                    Set-Location $currentDir
                    Write-Host "⚠️  Preserved $path (has uncommitted changes)" -ForegroundColor Yellow
                }
            } catch {
                Set-Location $currentDir
                Write-Host "⚠️  Preserved $path (error checking status)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "⚠️  Preserved $path (not a git repo)" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "✅ Uninstall complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To reinstall:" -ForegroundColor Cyan
Write-Host "powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or download fresh from GitHub:" -ForegroundColor Cyan
Write-Host 'Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/Install-ClaudeCodeDocs.ps1" -OutFile "Install-ClaudeCodeDocs.ps1"; powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1' -ForegroundColor Yellow