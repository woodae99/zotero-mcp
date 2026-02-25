@echo off
setlocal

REM Starts Zotero MCP in streamable HTTP mode for ChatGPT connector use.
REM Customize environment variables here if needed.

if "%ZOTERO_LOCAL%"=="" set ZOTERO_LOCAL=true

echo Starting zotero-mcp on http://127.0.0.1:8000 ...
zotero-mcp serve --transport streamable-http --host 127.0.0.1 --port 8000

endlocal
