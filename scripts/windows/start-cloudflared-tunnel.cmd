@echo off
setlocal

REM Starts a named Cloudflare tunnel to local Zotero MCP streamable HTTP port.
REM Requires an existing tunnel name in CLOUDFLARED_TUNNEL_NAME.

if "%CLOUDFLARED_TUNNEL_NAME%"=="" (
  echo ERROR: CLOUDFLARED_TUNNEL_NAME is not set.
  echo Example: set CLOUDFLARED_TUNNEL_NAME=zotero-mcp
  exit /b 1
)

echo Starting Cloudflare tunnel '%CLOUDFLARED_TUNNEL_NAME%' ...
cloudflared tunnel run %CLOUDFLARED_TUNNEL_NAME%

endlocal
