@echo off
setlocal

REM Runs the repo hygiene gate checks before MCP transport work.
REM Requires git in PATH.

echo [1/4] Current branch:
git branch --show-current
if errorlevel 1 goto :git_missing

echo.
echo [2/4] Working tree status:
git status --short --branch
if errorlevel 1 goto :git_error

echo.
echo [3/4] Fetch remotes:
git fetch --all --prune
if errorlevel 1 goto :git_error

echo.
echo [4/4] Divergence from origin/main:
git rev-list --left-right --count origin/main...HEAD
if errorlevel 1 goto :git_error

echo.
echo Preflight repo hygiene checks completed.
endlocal
exit /b 0

:git_missing
echo ERROR: git is not available in PATH.
endlocal
exit /b 2

:git_error
echo ERROR: git command failed.
endlocal
exit /b 1
