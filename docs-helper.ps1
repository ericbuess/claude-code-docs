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
        Write-Host "  * $name" -ForegroundColor Green
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