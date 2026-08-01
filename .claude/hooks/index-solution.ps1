#!/usr/bin/env pwsh
# Solution Indexer Hook for Claude Code
# Triggers after file modifications to rebuild solution index

param()

$ErrorActionPreference = "Stop"

# Configuration
$SOLUTION_ROOT = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { Get-Location }
$INDEX_FILE = Join-Path $SOLUTION_ROOT ".claude\solution-index.json"
$LOG_FILE = Join-Path $SOLUTION_ROOT ".claude\hooks\indexer.log"

# Ensure directories exist
$indexDir = Split-Path $INDEX_FILE -Parent
if (-not (Test-Path $indexDir)) {
    New-Item -ItemType Directory -Path $indexDir -Force | Out-Null
}

# Function to write log
function Write-IndexLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Add-Content -Path $LOG_FILE -ErrorAction SilentlyContinue
}

try {
    # Read hook input from stdin
    $inputJson = [Console]::In.ReadToEnd()
    $hookData = $inputJson | ConvertFrom-Json
    
    # Extract relevant information
    $toolName = $hookData.tool_name
    $toolInput = $hookData.tool_input
    $eventName = $hookData.hook_event_name
    
    Write-IndexLog "Hook triggered: $eventName for tool $toolName"
    
    # Determine which file was modified
    $modifiedFile = $null
    switch ($toolName) {
        "Write" { $modifiedFile = $toolInput.file_path }
        "Edit" { $modifiedFile = $toolInput.file_path }
        "MultiEdit" { $modifiedFile = $toolInput.file_path }
    }
    
    if ($modifiedFile) {
        Write-IndexLog "File modified: $modifiedFile"
    }
    
    # Start indexing in background (non-blocking)
    $indexJob = Start-Job -ScriptBlock {
        param($Root, $IndexFile, $LogFile)
        
        function Write-JobLog {
            param([string]$Message)
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            "$timestamp - [INDEXER] $Message" | Add-Content -Path $LogFile -ErrorAction SilentlyContinue
        }
        
        Write-JobLog "Starting solution index rebuild..."
        
        # Build the index
        $index = @{
            timestamp = (Get-Date).ToUniversalTime().ToString("o")
            root = $Root
            statistics = @{}
            files = @()
            structure = @{}
        }
        
        # Define file patterns to index
        $includePatterns = @(
            "*.cs", "*.vb", "*.fs",           # .NET languages
            "*.csproj", "*.vbproj", "*.fsproj", "*.sln",  # Project files
            "*.js", "*.jsx", "*.ts", "*.tsx",  # JavaScript/TypeScript
            "*.py",                             # Python
            "*.ps1", "*.psm1", "*.psd1",      # PowerShell
            "*.cpp", "*.hpp", "*.c", "*.h",    # C/C++
            "*.java",                           # Java
            "*.go",                             # Go
            "*.rs",                             # Rust
            "*.php",                            # PHP
            "*.rb",                             # Ruby
            "*.swift",                          # Swift
            "*.kt", "*.kts",                    # Kotlin
            "*.json", "*.xml", "*.yaml", "*.yml", # Config files
            "*.md", "*.txt",                    # Documentation
            "*.html", "*.css", "*.scss", "*.sass" # Web files
        )
        
        # Define directories to exclude
        $excludeDirs = @(
            ".git", ".svn", ".hg",
            "node_modules", "packages", ".nuget",
            "bin", "obj", "Debug", "Release",
            "dist", "build", "out",
            ".vs", ".vscode", ".idea",
            "__pycache__", ".pytest_cache",
            "venv", "env", ".env"
        )
        
        # Build exclude regex
        $excludeRegex = ($excludeDirs | ForEach-Object { [regex]::Escape($_) }) -join '|'
        $excludeRegex = "[\\/]($excludeRegex)[\\/]"
        
        # Collect all files
        $allFiles = @()
        foreach ($pattern in $includePatterns) {
            $files = Get-ChildItem -Path $Root -Filter $pattern -Recurse -File -ErrorAction SilentlyContinue |
                Where-Object { $_.FullName -notmatch $excludeRegex }
            $allFiles += $files
        }
        
        Write-JobLog "Found $($allFiles.Count) files to index"
        
        # Process files
        $filesByExtension = @{}
        $totalSize = 0
        
        foreach ($file in $allFiles) {
            $relativePath = $file.FullName.Substring($Root.Length).TrimStart('\', '/')
            $ext = $file.Extension.ToLower()
            
            # Track statistics
            if (-not $filesByExtension.ContainsKey($ext)) {
                $filesByExtension[$ext] = 0
            }
            $filesByExtension[$ext]++
            $totalSize += $file.Length
            
            # Add to index
            $index.files += @{
                path = $relativePath
                name = $file.Name
                extension = $ext
                size = $file.Length
                modified = $file.LastWriteTimeUtc.ToString("o")
                directory = (Split-Path $relativePath -Parent) -replace '\\', '/'
            }
        }
        
        # Build directory structure
        $dirs = @{}
        foreach ($file in $index.files) {
            $parts = $file.directory -split '/'
            $current = $dirs
            
            foreach ($part in $parts) {
                if ($part -and $part -ne ".") {
                    if (-not $current.ContainsKey($part)) {
                        $current[$part] = @{}
                    }
                    $current = $current[$part]
                }
            }
        }
        $index.structure = $dirs
        
        # Update statistics
        $index.statistics = @{
            totalFiles = $allFiles.Count
            totalSize = $totalSize
            totalSizeMB = [math]::Round($totalSize / 1MB, 2)
            filesByExtension = $filesByExtension
            lastUpdated = (Get-Date).ToUniversalTime().ToString("o")
        }
        
        # Look for solution files
        $slnFiles = Get-ChildItem -Path $Root -Filter "*.sln" -File -ErrorAction SilentlyContinue
        if ($slnFiles) {
            $index.solutions = $slnFiles | ForEach-Object {
                @{
                    name = $_.Name
                    path = $_.FullName.Substring($Root.Length).TrimStart('\', '/')
                }
            }
            Write-JobLog "Found $($slnFiles.Count) solution file(s)"
        }
        
        # Look for project files
        $projExtensions = @("*.csproj", "*.vbproj", "*.fsproj", "*.vcxproj", "*.pyproj", "*.njsproj")
        $projFiles = @()
        foreach ($ext in $projExtensions) {
            $projFiles += Get-ChildItem -Path $Root -Filter $ext -Recurse -File -ErrorAction SilentlyContinue |
                Where-Object { $_.FullName -notmatch $excludeRegex }
        }
        
        if ($projFiles) {
            $index.projects = $projFiles | ForEach-Object {
                @{
                    name = $_.BaseName
                    file = $_.Name
                    path = $_.FullName.Substring($Root.Length).TrimStart('\', '/')
                    type = $_.Extension.Substring(1, $_.Extension.Length - 5)  # Remove . and proj
                }
            }
            Write-JobLog "Found $($projFiles.Count) project file(s)"
        }
        
        # Save index
        $index | ConvertTo-Json -Depth 10 -Compress | Set-Content -Path $IndexFile -Encoding UTF8
        Write-JobLog "Index saved to $IndexFile"
        Write-JobLog "Indexing complete: $($index.statistics.totalFiles) files, $($index.statistics.totalSizeMB) MB"
        
        return @{
            success = $true
            filesIndexed = $index.statistics.totalFiles
            sizeMB = $index.statistics.totalSizeMB
        }
        
    } -ArgumentList $SOLUTION_ROOT, $INDEX_FILE, $LOG_FILE
    
    # Don't wait for job to complete (non-blocking)
    Write-IndexLog "Indexing job started with ID: $($indexJob.Id)"
    
    # Optional: Clean up old completed jobs
    Get-Job | Where-Object { $_.State -eq 'Completed' -and $_.Name -notlike 'IndexJob*' } | Remove-Job -Force -ErrorAction SilentlyContinue
    
    # Success - hook completes immediately while indexing continues in background
    Write-Host "Solution indexing started in background (Job ID: $($indexJob.Id))"
    exit 0
    
} catch {
    Write-IndexLog "ERROR: $_"
    Write-Error "Hook failed: $_"
    exit 1
}