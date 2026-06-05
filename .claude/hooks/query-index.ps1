#!/usr/bin/env pwsh
# Query Solution Index
# Helper script to query the solution index created by the indexer hook

param(
    [Parameter(Position=0)]
    [string]$Query = "",
    
    [Parameter()]
    [ValidateSet("files", "stats", "projects", "structure", "recent", "large")]
    [string]$Mode = "files"
)

$ErrorActionPreference = "Stop"

# Configuration
$SOLUTION_ROOT = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { Get-Location }
$INDEX_FILE = Join-Path $SOLUTION_ROOT ".claude\solution-index.json"

if (-not (Test-Path $INDEX_FILE)) {
    Write-Host "No index found. The index will be created after file modifications." -ForegroundColor Yellow
    Write-Host "Index location: $INDEX_FILE"
    exit 1
}

# Load index
$index = Get-Content $INDEX_FILE -Raw | ConvertFrom-Json

Write-Host "Solution Index - $($index.root)" -ForegroundColor Cyan
Write-Host "Last updated: $($index.statistics.lastUpdated)" -ForegroundColor Gray
Write-Host ""

switch ($Mode) {
    "stats" {
        Write-Host "Statistics:" -ForegroundColor Green
        Write-Host "  Total files: $($index.statistics.totalFiles)"
        Write-Host "  Total size: $($index.statistics.totalSizeMB) MB"
        Write-Host ""
        Write-Host "Files by extension:" -ForegroundColor Green
        $index.statistics.filesByExtension.PSObject.Properties | 
            Sort-Object -Property Value -Descending |
            Select-Object -First 15 |
            ForEach-Object {
                Write-Host ("  {0,-10} {1,6} files" -f $_.Name, $_.Value)
            }
        
        if ($index.solutions) {
            Write-Host ""
            Write-Host "Solutions:" -ForegroundColor Green
            $index.solutions | ForEach-Object {
                Write-Host "  $($_.name)"
            }
        }
    }
    
    "projects" {
        if ($index.projects) {
            Write-Host "Projects:" -ForegroundColor Green
            $index.projects | 
                Sort-Object -Property type, name |
                ForEach-Object {
                    Write-Host ("  [{0,-6}] {1}" -f $_.type.ToUpper(), $_.name)
                    Write-Host ("           {0}" -f $_.path) -ForegroundColor Gray
                }
        } else {
            Write-Host "No project files found in index" -ForegroundColor Yellow
        }
    }
    
    "structure" {
        function Show-Tree {
            param($Node, $Indent = "")
            
            foreach ($key in $Node.PSObject.Properties.Name | Sort-Object) {
                Write-Host "$Indent├── $key" -ForegroundColor DarkCyan
                if ($Node.$key -and $Node.$key.PSObject.Properties.Count -gt 0) {
                    Show-Tree -Node $Node.$key -Indent "$Indent│   "
                }
            }
        }
        
        Write-Host "Directory Structure:" -ForegroundColor Green
        Show-Tree -Node $index.structure
    }
    
    "recent" {
        Write-Host "Recently Modified Files (last 20):" -ForegroundColor Green
        $index.files | 
            Sort-Object -Property modified -Descending |
            Select-Object -First 20 |
            ForEach-Object {
                $modified = [DateTime]::Parse($_.modified).ToLocalTime().ToString("yyyy-MM-dd HH:mm")
                Write-Host ("  {0} - {1}" -f $modified, $_.path)
            }
    }
    
    "large" {
        Write-Host "Largest Files (top 20):" -ForegroundColor Green
        $index.files | 
            Sort-Object -Property size -Descending |
            Select-Object -First 20 |
            ForEach-Object {
                $sizeMB = [math]::Round($_.size / 1MB, 2)
                Write-Host ("  {0,8} MB - {1}" -f $sizeMB, $_.path)
            }
    }
    
    "files" {
        if ($Query) {
            Write-Host "Searching for: '$Query'" -ForegroundColor Green
            $matches = $index.files | Where-Object { 
                $_.path -like "*$Query*" -or 
                $_.name -like "*$Query*" 
            }
            
            if ($matches) {
                Write-Host "Found $($matches.Count) matches:" -ForegroundColor Green
                $matches | Select-Object -First 50 | ForEach-Object {
                    Write-Host "  $($_.path)"
                }
                
                if ($matches.Count -gt 50) {
                    Write-Host "  ... and $($matches.Count - 50) more" -ForegroundColor Gray
                }
            } else {
                Write-Host "No files matching '$Query'" -ForegroundColor Yellow
            }
        } else {
            Write-Host "File Extensions in Project:" -ForegroundColor Green
            $extensions = $index.files | 
                Group-Object -Property extension | 
                Sort-Object -Property Count -Descending |
                Select-Object -First 20
            
            $extensions | ForEach-Object {
                Write-Host ("  {0,-10} {1,6} files" -f $_.Name, $_.Count)
            }
            
            Write-Host ""
            Write-Host "Use -Query parameter to search for specific files" -ForegroundColor Gray
            Write-Host "Example: .\query-index.ps1 -Query 'controller' -Mode files" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "Other modes: -Mode [stats|projects|structure|recent|large|files]" -ForegroundColor Gray