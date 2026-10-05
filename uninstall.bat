@echo off
REM Claude Code Docs Uninstaller for Windows - Batch Wrapper
REM This batch file makes it easy to run the PowerShell uninstaller

echo ============================================
echo  Claude Code Docs Uninstaller for Windows
echo ============================================
echo.
echo This will remove:
echo   - The /docs command
echo   - Auto-update hooks from Claude settings
echo   - Installation directory at %USERPROFILE%\.claude-code-docs
echo.
echo Your documentation files will be permanently deleted.
echo.

set /p confirm="Are you sure you want to uninstall? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo Starting uninstallation...
echo.

REM Check if uninstaller exists in current directory
if exist "%~dp0Uninstall-ClaudeCodeDocs.ps1" (
    REM Run from current directory
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Uninstall-ClaudeCodeDocs.ps1" -Force
) else if exist "%USERPROFILE%\.claude-code-docs\Uninstall-ClaudeCodeDocs.ps1" (
    REM Run from installation directory
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\.claude-code-docs\Uninstall-ClaudeCodeDocs.ps1" -Force
) else (
    echo.
    echo ERROR: Uninstaller script not found!
    echo.
    echo To manually uninstall:
    echo   1. Delete %USERPROFILE%\.claude-code-docs
    echo   2. Delete %USERPROFILE%\.claude\commands\docs.md
    echo   3. Remove claude-code-docs hooks from %USERPROFILE%\.claude\settings.json
    echo.
    pause
    exit /b 1
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================
    echo  Uninstallation failed with error code %ERRORLEVEL%
    echo ============================================
    echo.
    echo Some components may not have been removed.
    echo Check the README-WINDOWS.md for manual uninstall instructions.
    echo.
) else (
    echo.
    echo ============================================
    echo  Uninstallation completed successfully!
    echo ============================================
    echo.
    echo Claude Code Documentation Mirror has been removed.
    echo.
    echo To reinstall later, run install.bat or use:
    echo   powershell.exe -ExecutionPolicy Bypass -File Install-ClaudeCodeDocs.ps1
    echo.
)

pause