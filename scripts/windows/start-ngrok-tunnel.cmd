@echo off
setlocal

REM Starts an ngrok HTTPS tunnel to local Zotero MCP streamable HTTP port.
REM Requires NGROK_DOMAIN to be set to a reserved ngrok domain.

if "%NGROK_DOMAIN%"=="" (
  echo ERROR: NGROK_DOMAIN is not set.
  echo Example: set NGROK_DOMAIN=your-name.ngrok-free.app
  exit /b 1
)

echo Starting ngrok tunnel for https://%NGROK_DOMAIN% -> http://127.0.0.1:8000
ngrok http --domain=%NGROK_DOMAIN% 8000

endlocal
