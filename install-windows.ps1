# Claude Code Docs Installer for Windows
# PowerShell port of the bash installer
# Version: 0.3.3-windows

Write-Host "Claude Code Docs Installer for Windows v0.3.3" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

$INSTALL_DIR = "$env:USERPROFILE\.claude-code-docs"
$CLAUDE_DIR = "$env:USERPROFILE\.claude"
$COMMANDS_DIR = "$CLAUDE_DIR\commands"

# Check if Git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Git is not installed" -ForegroundColor Red
    Write-Host "Please install Git for Windows from https://git-scm.com/download/win"
    exit 1
}

Write-Host "✓ Git is installed" -ForegroundColor Green

# Check if directory already exists
if (Test-Path $INSTALL_DIR) {
    Write-Host "✓ Found installation at $INSTALL_DIR" -ForegroundColor Green
    Write-Host "  Updating to latest version..." -ForegroundColor Gray
    
    Push-Location $INSTALL_DIR
    try {
        git pull origin main 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  Standard update failed, forcing clean state..." -ForegroundColor Yellow
            git fetch origin main
            git reset --hard origin/main
        }
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host "No existing installation found" -ForegroundColor Yellow
    Write-Host "Installing fresh to $INSTALL_DIR..." -ForegroundColor Gray
    
    # Clone the repository
    git clone https://github.com/ericbuess/claude-code-docs.git $INSTALL_DIR
}

Write-Host ""
Write-Host "Setting up Claude Code Docs for Windows..." -ForegroundColor Cyan

# Create the PowerShell helper script
$helperScript = @'
# Windows PowerShell Docs Helper
param(
    [string]$Command = ""
)

$docsPath = "$env:USERPROFILE\.claude-code-docs\docs"

# Handle hook-check
if ($Command -eq "hook-check") {
    exit 0
}

# Show topics if no command
if ([string]::IsNullOrEmpty($Command)) {
    Write-Host "COMMUNITY MIRROR: https://github.com/ericbuess/claude-code-docs" -ForegroundColor Cyan
    Write-Host "OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available documentation topics:" -ForegroundColor Yellow
    
    $files = Get-ChildItem -Path $docsPath -Filter "*.md" | Sort-Object Name
    foreach ($file in $files) {
        $name = $file.BaseName
        Write-Host "  • $name" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Usage: /docs <topic> to read documentation" -ForegroundColor Gray
    exit 0
}

# Check for freshness flag
if ($Command -eq "-t") {
    Push-Location "$env:USERPROFILE\.claude-code-docs"
    git fetch origin main 2>&1 | Out-Null
    $behind = git rev-list HEAD..origin/main --count 2>&1
    if ($LASTEXITCODE -eq 0 -and $behind -gt 0) {
        Write-Host "Documentation is $behind commits behind. Updating..." -ForegroundColor Yellow
        git pull origin main
    } else {
        Write-Host "Documentation is up to date" -ForegroundColor Green
    }
    Pop-Location
    exit 0
}

# Read specific doc
$filePath = "$docsPath\$Command.md"
if (Test-Path $filePath) {
    Write-Host "COMMUNITY MIRROR: https://github.com/ericbuess/claude-code-docs" -ForegroundColor Cyan
    Write-Host "OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code" -ForegroundColor Cyan
    Write-Host ""
    
    Get-Content $filePath
    
    Write-Host ""
    Write-Host "Official page: https://docs.anthropic.com/en/docs/claude-code/$Command" -ForegroundColor Cyan
} else {
    Write-Host "Documentation for '$Command' not found" -ForegroundColor Red
    Write-Host "Run /docs to see available topics" -ForegroundColor Yellow
}
'@

$helperScript | Out-File -FilePath "$INSTALL_DIR\docs-helper.ps1" -Encoding UTF8
Write-Host "✓ Created Windows helper script" -ForegroundColor Green

# Create /docs command
Write-Host "Setting up /docs command..." -ForegroundColor Yellow

if (!(Test-Path $COMMANDS_DIR)) {
    New-Item -ItemType Directory -Path $COMMANDS_DIR -Force | Out-Null
}

$commandContent = @'
Execute the Claude Code Docs PowerShell script for Windows

Usage:
- /docs - List all available documentation topics
- /docs <topic> - Read specific documentation
- /docs -t - Check if documentation is up to date
- /docs -t <topic> - Update and read documentation

Examples:
  /docs hooks       # Read hooks documentation
  /docs mcp         # Read MCP documentation
  /docs settings    # Read settings documentation
  /docs -t          # Check for updates

📚 COMMUNITY MIRROR: https://github.com/ericbuess/claude-code-docs
📖 OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code

Execute: powershell -ExecutionPolicy Bypass -File "C:\Users\$env:USERNAME\.claude-code-docs\docs-helper.ps1" "$ARGUMENTS"
'@

$commandContent | Out-File -FilePath "$COMMANDS_DIR\docs.md" -Encoding UTF8
Write-Host "✓ Created /docs command" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Claude Code Docs installed successfully for Windows!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Command: /docs (user)" -ForegroundColor Cyan
Write-Host "📂 Location: $INSTALL_DIR" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available topics:" -ForegroundColor Yellow

$topics = Get-ChildItem -Path "$INSTALL_DIR\docs" -Filter "*.md" | Select-Object -ExpandProperty BaseName | Sort-Object
$topics -join ", "

Write-Host ""
Write-Host "⚠️  Note: Restart Claude Code for changes to take effect" -ForegroundColor Yellow