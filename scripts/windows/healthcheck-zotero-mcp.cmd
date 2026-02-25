@echo off
setlocal

REM Health check for local and remote Zotero MCP endpoints.
REM Usage:
REM   healthcheck-zotero-mcp.cmd
REM   healthcheck-zotero-mcp.cmd https://your-mcp-hostname

set LOCAL_URL=http://127.0.0.1:8000/
set REMOTE_URL=%1

echo Checking local endpoint: %LOCAL_URL%
call :check_url %LOCAL_URL%
if errorlevel 1 (
  echo FAIL: local endpoint is not reachable.
  exit /b 1
) else (
  echo OK: local endpoint reachable.
)

if not "%REMOTE_URL%"=="" (
  echo Checking remote endpoint: %REMOTE_URL%
  call :check_url %REMOTE_URL%
  if errorlevel 1 (
    echo FAIL: remote endpoint is not reachable.
    exit /b 2
  ) else (
    echo OK: remote endpoint reachable.
  )
)

echo Health check completed.
endlocal
exit /b 0

:check_url
set URL=%1
powershell -NoProfile -Command "try { Invoke-WebRequest -UseBasicParsing -Method Head -Uri '%URL%' -TimeoutSec 8 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 exit /b 0

curl -sS -I %URL% >nul 2>&1
if not errorlevel 1 exit /b 0

exit /b 1
