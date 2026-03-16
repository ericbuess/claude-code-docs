@echo off
REM Claude Code Docs Installer for Windows - Batch Wrapper
REM This batch file makes it easy to run the PowerShell installer

echo ============================================
echo  Claude Code Docs Installer for Windows
echo ============================================
echo.
echo This will install Claude Code Documentation Mirror to:
echo   %USERPROFILE%\.claude-code-docs
echo.
echo Prerequisites:
echo   - Git for Windows must be installed
echo   - PowerShell 5.1 or higher (comes with Windows 10/11)
echo.
pause

echo.
echo Starting installation...
echo.

REM Check if PowerShell script exists in current directory
if exist "%~dp0Install-ClaudeCodeDocs.ps1" (
    REM Run from current directory
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-ClaudeCodeDocs.ps1"
) else (
    REM Try to download from GitHub
    echo PowerShell installer not found locally.
    echo Downloading from GitHub...
    powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/Install-ClaudeCodeDocs.ps1' -OutFile '%TEMP%\Install-ClaudeCodeDocs.ps1'; & '%TEMP%\Install-ClaudeCodeDocs.ps1'; Remove-Item '%TEMP%\Install-ClaudeCodeDocs.ps1' }"
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================
    echo  Installation failed with error code %ERRORLEVEL%
    echo ============================================
    echo.
    echo Troubleshooting:
    echo   1. Make sure Git for Windows is installed
    echo   2. Check your internet connection
    echo   3. Try running as Administrator
    echo   4. Check the README-WINDOWS.md for more help
    echo.
) else (
    echo.
    echo ============================================
    echo  Installation completed successfully!
    echo ============================================
    echo.
    echo Next steps:
    echo   1. Restart Claude Code
    echo   2. Use /docs command to access documentation
    echo.
    echo Examples:
    echo   /docs           - List all topics
    echo   /docs hooks     - Read hooks documentation
    echo   /docs -t        - Check for updates
    echo.
)

pause