# ChatGPT Desktop (Windows) with Local Zotero MCP over HTTPS

This guide implements a local-laptop-first setup:

- Zotero MCP runs on your laptop
- Transport is `streamable-http`
- ChatGPT reaches it through a stable HTTPS tunnel endpoint
- No OAuth for this version

## 1. Preconditions

1. Install and configure `zotero-mcp-server`.
2. Ensure Zotero is installed and local API access is enabled.
3. Ensure ChatGPT Developer Mode is available on your account.
4. Install `cloudflared` or `ngrok` on Windows.

## 1.5 Repo hygiene preflight

Run this before setup work if you are making repo changes:

```bat
scripts\windows\preflight-repo-hygiene.cmd
```

Expected checks:

1. Current branch
2. `git status --short --branch`
3. `git fetch --all --prune`
4. `git rev-list --left-right --count origin/main...HEAD`

## 2. Start MCP in streamable HTTP mode

Run this command in a terminal and keep it running:

```bat
zotero-mcp serve --transport streamable-http --host 127.0.0.1 --port 8000
```

Or use the helper script:

```bat
scripts\windows\start-zotero-mcp-http.cmd
```

## 3. Expose HTTPS endpoint (stable URL)

You need an HTTPS endpoint that stays consistent so you do not have to recreate the connector.

### Option A: Cloudflare Tunnel (recommended for stable hostname)

```bat
cloudflared tunnel run zotero-mcp
```

Tunnel config should point to:

- `http://127.0.0.1:8000`

Or use the helper script:

```bat
set CLOUDFLARED_TUNNEL_NAME=zotero-mcp
scripts\windows\start-cloudflared-tunnel.cmd
```

### Option B: ngrok (reserved domain)

```bat
ngrok http --domain=<your-reserved-domain> 8000
```

Or use the helper script:

```bat
set NGROK_DOMAIN=<your-reserved-domain>
scripts\windows\start-ngrok-tunnel.cmd
```

## 4. Configure ChatGPT connector

In ChatGPT Developer Mode:

1. Go to `Settings -> Connectors -> Create`.
2. Set name/description.
3. Set MCP URL to your HTTPS tunnel URL.
4. Authentication: `None`.
5. Save and verify tool discovery.

## 5. Validate end-to-end

Use this checklist:

1. Server startup succeeds on `127.0.0.1:8000`.
2. HTTPS endpoint is reachable from browser.
3. Connector creation succeeds.
4. Tools are listed in ChatGPT.
5. `search` tool returns Zotero results.
6. `fetch` tool returns metadata/fulltext.

## 6. Auto-start for travel laptops

Use Task Scheduler to run both processes at logon:

1. Task `zotero-mcp-http`
2. Task `zotero-mcp-tunnel`

Set each task to:

- Run whether user is logged on or not
- Restart on failure
- Start when available after missed start

Example `schtasks` commands for MCP server startup (replace `<REPO_PATH>` with your absolute path, e.g. `C:\Users\colin\Dev\GitHub\zotero-mcp`):

```bat
schtasks /Create /TN "zotero-mcp-http" /SC ONLOGON /TR "\"<REPO_PATH>\\scripts\\windows\\start-zotero-mcp-http.cmd\"" /RL HIGHEST /F
```

For tunnel startup, choose one:

```bat
schtasks /Create /TN "zotero-mcp-tunnel-cloudflared" /SC ONLOGON /TR "\"<REPO_PATH>\\scripts\\windows\\start-cloudflared-tunnel.cmd\"" /RL HIGHEST /F
```

```bat
schtasks /Create /TN "zotero-mcp-tunnel-ngrok" /SC ONLOGON /TR "\"<REPO_PATH>\\scripts\\windows\\start-ngrok-tunnel.cmd\"" /RL HIGHEST /F
```

## 7. Health checks and recovery

Basic local check:

```bat
curl -I http://127.0.0.1:8000/
```

Basic HTTPS check:

```bat
curl -I https://<your-mcp-hostname>/
```

Or use:

```bat
scripts\windows\healthcheck-zotero-mcp.cmd https://<your-mcp-hostname>/
```

Recovery sequence:

1. Ensure Zotero desktop is running.
2. Restart `zotero-mcp` process.
3. Restart tunnel process.
4. Re-test connector in ChatGPT.

## 8. Offline fallback

If you do not have internet/public reachability, use local MCP clients with `stdio`:

```bat
zotero-mcp serve --transport stdio
```

This keeps local workflows available in tools that support direct local MCP processes.
