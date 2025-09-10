# Claude Code Documentation Helper Script for Windows v0.3.3
# PowerShell port of the original bash helper script
# This script handles all /docs command functionality
# Installation path: $env:USERPROFILE\.claude-code-docs\claude-docs-helper.ps1

param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ErrorActionPreference = "Stop"
$Script:Version = "0.3.3-windows"

# Fixed installation path
$DOCS_PATH = Join-Path $env:USERPROFILE ".claude-code-docs"
$MANIFEST = Join-Path $DOCS_PATH "docs\docs_manifest.json"

# Function to sanitize input (prevent command injection)
function Sanitize-Input {
    param([string]$Input)
    
    # Remove all shell metacharacters and control characters
    # Only allow alphanumeric, spaces, hyphens, underscores, periods, commas, apostrophes, and question marks
    $sanitized = $Input -replace "[^a-zA-Z0-9 _.,'\?-]", ""
    $sanitized = $sanitized -replace "\s+", " "
    $sanitized = $sanitized.Trim()
    return $sanitized
}

# Function to print documentation header
function Show-DocHeader {
    Write-Host "COMMUNITY MIRROR: https://github.com/ericbuess/claude-code-docs"
    Write-Host "OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code"
    Write-Host ""
}

# Function to auto-update docs if needed
function Update-Docs {
    try {
        Set-Location $DOCS_PATH -ErrorAction SilentlyContinue
        if ($LASTEXITCODE -ne 0) { return 1 }
        
        # Get current branch
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        if (-not $branch) { $branch = "main" }
        
        # Quick fetch to check for updates
        git fetch --quiet origin $branch 2>$null
        if ($LASTEXITCODE -ne 0) {
            # Try main if current branch doesn't exist
            git fetch --quiet origin main 2>$null
            if ($LASTEXITCODE -ne 0) {
                return 2  # Can't sync
            }
            $branch = "main"
        }
        
        $local = git rev-parse HEAD 2>$null
        $remote = git rev-parse "origin/$branch" 2>$null
        
        # Check if we're behind remote
        $behind = git rev-list "HEAD..origin/$branch" --count 2>$null
        if (-not $behind) { $behind = 0 }
        
        if (($local -ne $remote) -and ($behind -gt 0)) {
            # We're behind - safe to pull
            Write-Host "Updating documentation..." -ForegroundColor Yellow
            git pull --quiet origin $branch 2>&1 | Where-Object { $_ -notmatch "Merge made by" } | Out-Null
            
            # Check if installer needs updating
            $versionInt = [int]($Script:Version -replace "^0\.", "" -replace "-windows", "")
            
            if ($versionInt -ge 3) {
                Write-Host "Updating Claude Code Docs installer..." -ForegroundColor Yellow
                & (Join-Path $DOCS_PATH "Install-ClaudeCodeDocs.ps1") 2>&1 | Out-Null
            }
        }
        
        return 0  # Success
    } catch {
        return 1
    }
}

# Function to show documentation sync status
function Show-Freshness {
    Show-DocHeader
    
    # Read manifest
    if (-not (Test-Path $MANIFEST)) {
        Write-Host "ERROR: Documentation not found at $env:USERPROFILE\.claude-code-docs" -ForegroundColor Red
        Write-Host "Please reinstall with:" -ForegroundColor Yellow
        Write-Host "powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1" -ForegroundColor Cyan
        exit 1
    }
    
    # Try to sync with GitHub
    $syncStatus = Update-Docs
    
    if ($syncStatus -eq 2) {
        Write-Host "WARNING: Could not sync with GitHub (using local cache)" -ForegroundColor Yellow
        Write-Host "Check your internet connection or GitHub access" -ForegroundColor Yellow
    } else {
        # Check if we're ahead or behind
        try {
            Set-Location $DOCS_PATH
            $branch = git rev-parse --abbrev-ref HEAD 2>$null
            if (-not $branch) { $branch = "main" }
            
            $compareBranch = $branch
            git rev-parse --verify "origin/$branch" 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) {
                $compareBranch = "main"
            }
            
            $ahead = git rev-list "origin/${compareBranch}..HEAD" --count 2>$null
            if (-not $ahead) { $ahead = 0 }
            $behind = git rev-list "HEAD..origin/$compareBranch" --count 2>$null
            if (-not $behind) { $behind = 0 }
            
            if ($ahead -gt 0) {
                Write-Host "WARNING: Local version is ahead of GitHub by $ahead commit(s)" -ForegroundColor Yellow
            } elseif ($behind -gt 0) {
                Write-Host "WARNING: Local version is behind GitHub by $behind commit(s)" -ForegroundColor Yellow
            } else {
                Write-Host "OK: You have the latest documentation" -ForegroundColor Green
            }
        } catch {
            Write-Host "WARNING: Could not determine sync status" -ForegroundColor Yellow
        }
    }
    
    # Show current branch and version
    try {
        Set-Location $DOCS_PATH
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        if (-not $branch) { $branch = "unknown" }
        Write-Host "Branch: $branch"
        Write-Host "Version: $($Script:Version)"
    } catch {
        Write-Host "Version: $($Script:Version)"
    }
}

# Function to read documentation
function Read-Doc {
    param([string]$Topic)
    
    $topic = Sanitize-Input $Topic
    
    # Strip .md extension if user included it
    $topic = $topic -replace "\.md$", ""
    
    $docPath = Join-Path $DOCS_PATH "docs\$topic.md"
    
    if (Test-Path $docPath) {
        Show-DocHeader
        
        # Quick check if we're up to date
        try {
            Set-Location $DOCS_PATH
            $branch = git rev-parse --abbrev-ref HEAD 2>$null
            if (-not $branch) { $branch = "main" }
            
            # Do the fetch to check status
            $compareBranch = $branch
            git fetch --quiet origin $branch 2>$null
            if ($LASTEXITCODE -ne 0) {
                git fetch --quiet origin main 2>$null
                if ($LASTEXITCODE -eq 0) {
                    $compareBranch = "main"
                } else {
                    Write-Host "WARNING: Could not check GitHub for updates - using cached docs (v$($Script:Version), ${branch})" -ForegroundColor Yellow
                    Write-Host ""
                    Get-Content $docPath -Raw
                    Write-Host ""
                    Write-Host "Official page: https://docs.anthropic.com/en/docs/claude-code/$topic"
                    return
                }
            }
            
            $local = git rev-parse HEAD 2>$null
            $remote = git rev-parse "origin/$compareBranch" 2>$null
            $behind = git rev-list "HEAD..origin/$compareBranch" --count 2>$null
            if (-not $behind) { $behind = 0 }
            
            if (($local -ne $remote) -and ($behind -gt 0)) {
                # We're behind - safe to update
                Write-Host "Updating to latest documentation..." -ForegroundColor Yellow
                git pull --quiet origin $compareBranch 2>&1 | Where-Object { $_ -notmatch "Merge made by" } | Out-Null
                
                # Check if installer needs updating
                $versionInt = [int]($Script:Version -replace "^0\.", "" -replace "-windows", "")
                if ($versionInt -ge 3) {
                    & (Join-Path $DOCS_PATH "Install-ClaudeCodeDocs.ps1") 2>&1 | Out-Null
                }
                Write-Host "OK: Updated to latest (v$($Script:Version), ${branch})" -ForegroundColor Green
            } else {
                $ahead = git rev-list "origin/${compareBranch}..HEAD" --count 2>$null
                if (-not $ahead) { $ahead = 0 }
                if ($ahead -gt 0) {
                    Write-Host "WARNING: Using local development version (v$($Script:Version), ${branch}, +${ahead} commits)" -ForegroundColor Yellow
                } else {
                    Write-Host "OK: You have the latest docs (v$($Script:Version), ${branch})" -ForegroundColor Green
                }
            }
        } catch {
            Write-Host "WARNING: Could not check for updates" -ForegroundColor Yellow
        }
        
        Write-Host ""
        Get-Content $docPath -Raw
        Write-Host ""
        
        if ($topic -eq "changelog") {
            Write-Host "Official source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
        } else {
            Write-Host "Official page: https://docs.anthropic.com/en/docs/claude-code/$topic"
        }
    } else {
        # Always show search interface
        Show-DocHeader
        Write-Host "Searching for: $topic"
        Write-Host ""
        
        # Try to extract keywords from the topic
        $keywords = ($topic -split '\s+' | Where-Object { 
            $_ -notmatch '^(tell|me|about|explain|what|is|are|how|do|to|show|find|search|the|for|in)$' 
        }) -join '|'
        
        if ($keywords) {
            # Search for matching topics
            $docs = Get-ChildItem (Join-Path $DOCS_PATH "docs") -Filter "*.md" | 
                ForEach-Object { $_.BaseName }
            
            $matches = $docs | Where-Object { $_ -match $keywords }
            
            if ($matches) {
                Write-Host "Found these related topics:"
                $matches | ForEach-Object { Write-Host "  • $_" }
                Write-Host ""
                Write-Host "Try: /docs 'topic' to read a specific document"
            } else {
                Write-Host "No exact matches found. Here are all available topics:"
                $docs | Sort-Object | Format-Wide -Column 3
            }
        } else {
            Write-Host "Available topics:"
            Get-ChildItem (Join-Path $DOCS_PATH "docs") -Filter "*.md" | 
                ForEach-Object { $_.BaseName } | 
                Sort-Object | 
                Format-Wide -Column 3
        }
        Write-Host ""
        Write-Host "Tip: Use PowerShell to search across all docs:"
        Write-Host "   Get-ChildItem '$env:USERPROFILE\.claude-code-docs\docs' -Filter '*.md' | Select-String 'search term'"
    }
}

# Function to list available documentation
function Show-DocsList {
    Show-DocHeader
    
    # Auto-update to ensure fresh list
    Update-Docs | Out-Null
    
    Write-Host "Available documentation topics:"
    Write-Host ""
    Get-ChildItem (Join-Path $DOCS_PATH "docs") -Filter "*.md" | 
        ForEach-Object { $_.BaseName } | 
        Sort-Object | 
        Format-Wide -Column 3
    Write-Host ""
    Write-Host "Usage: /docs 'topic' or /docs -t to check freshness"
}

# Function for hook check (auto-update)
function Invoke-HookCheck {
    # This is now just a passthrough since Update-Docs handles everything
    exit 0
}

# Function to show what's new
function Show-WhatsNew {
    Show-DocHeader
    
    # Auto-update first
    Update-Docs | Out-Null
    
    try {
        Set-Location $DOCS_PATH
        
        Write-Host "Recent documentation updates:"
        Write-Host ""
        
        # Get recent commits
        $commits = git log --oneline -10 -- "docs/*.md" 2>$null | Where-Object { $_ -notmatch "Merge" }
        $count = 0
        
        foreach ($commitLine in $commits) {
            if ($count -ge 5) { break }
            
            $hash = ($commitLine -split ' ')[0]
            $date = git show -s --format=%cr $hash 2>$null
            if (-not $date) { $date = "unknown" }
            
            Write-Host "• ${date}:"
            Write-Host "  Commit: https://github.com/ericbuess/claude-code-docs/commit/$hash"
            
            # Show which docs changed
            $changedDocs = git diff-tree --no-commit-id --name-only -r $hash -- "docs/*.md" 2>$null | 
                ForEach-Object { 
                    $_ -replace "docs[/\\]", "" -replace "\.md$", ""
                } | Select-Object -First 5
            
            if ($changedDocs) {
                foreach ($doc in $changedDocs) {
                    if ($doc) {
                        Write-Host "  - ${doc}: https://docs.anthropic.com/en/docs/claude-code/$doc"
                    }
                }
            }
            Write-Host ""
            $count++
        }
        
        if ($count -eq 0) {
            Write-Host "No recent documentation updates found."
            Write-Host ""
        }
        
        Write-Host "Full changelog: https://github.com/ericbuess/claude-code-docs/commits/main/docs"
        Write-Host "COMMUNITY MIRROR - NOT AFFILIATED WITH ANTHROPIC"
    } catch {
        Write-Host "Error retrieving recent updates" -ForegroundColor Red
    }
}

# Function for uninstall
function Show-UninstallInstructions {
    Show-DocHeader
    Write-Host "To uninstall Claude Code Documentation Mirror"
    Write-Host "==========================================="
    Write-Host ""
    
    Write-Host "This will remove:"
    Write-Host "  • The /docs command from $env:USERPROFILE\.claude\commands\docs.md"
    Write-Host "  • The auto-update hook from $env:USERPROFILE\.claude\settings.json"
    Write-Host "  • The installation directory $env:USERPROFILE\.claude-code-docs"
    Write-Host ""
    
    Write-Host "Run this command in PowerShell:"
    Write-Host ""
    Write-Host "  & `"$env:USERPROFILE\.claude-code-docs\Uninstall-ClaudeCodeDocs.ps1`""
    Write-Host ""
    Write-Host "Or to skip confirmation:"
    Write-Host "  & `"$env:USERPROFILE\.claude-code-docs\Uninstall-ClaudeCodeDocs.ps1`" -Force"
    Write-Host ""
}

# Main command handling
$fullArgs = $Arguments -join " "

# Check for flags first
if ($fullArgs -match "^-t(\s+(.*))?$") {
    Show-Freshness
    $remainingArgs = $Matches[2]
    if ($remainingArgs -match "what.?s?\s?new") {
        Write-Host ""
        Show-WhatsNew
    } elseif ($remainingArgs) {
        Write-Host ""
        Read-Doc -Topic $remainingArgs
    }
    exit 0
} elseif ($fullArgs -match "^--check(\s+(.*))?$") {
    Show-Freshness
    $remainingArgs = $Matches[2]
    if ($remainingArgs -match "what.?s?\s?new") {
        Write-Host ""
        Show-WhatsNew
    } elseif ($remainingArgs) {
        Write-Host ""
        Read-Doc -Topic $remainingArgs
    }
    exit 0
}

# Handle main commands
$firstArg = if ($Arguments -and $Arguments.Count -gt 0) { $Arguments[0] } else { "" }
switch -Regex ($firstArg) {
    "^$" {
        Show-DocsList
    }
    "^-t$|^--check$" {
        Show-Freshness
        if ($Arguments.Count -gt 1) {
            $remaining = ($Arguments[1..($Arguments.Count-1)] -join " ")
            if ($remaining -match "what.?s?\s?new") {
                Write-Host ""
                Show-WhatsNew
            } else {
                Write-Host ""
                Read-Doc -Topic $remaining
            }
        }
    }
    "^hook-check$" {
        Invoke-HookCheck
    }
    "^uninstall$" {
        Show-UninstallInstructions
    }
    "^whats-new$|^whats$|^what$" {
        $remaining = if ($Arguments.Count -gt 1) { 
            ($Arguments[1..($Arguments.Count-1)] -join " ") 
        } else { 
            "" 
        }
        if ($remaining -match "new" -or $fullArgs -match "what.*new") {
            Show-WhatsNew
        } else {
            Read-Doc -Topic $Arguments[0]
        }
    }
    default {
        # Check if the full arguments match "what's new" pattern
        if ($fullArgs -match "what.*new") {
            Show-WhatsNew
        } else {
            # Default: read documentation
            Read-Doc -Topic $fullArgs
        }
    }
}

# Ensure script always exits successfully
exit 0