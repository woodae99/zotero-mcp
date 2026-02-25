# OpenMemory Guide

## Overview
- Project: `zotero-mcp`
- Purpose: MCP server for Zotero read/write, annotations, notes, collections, and search workflows.
- Latest validation artifact: `docs/zotero-mcp-tooling-test-report-2026-02-21.md`.

## Architecture
- Core server implementation: `src/zotero_mcp/server.py`
- Client and integration helpers: `src/zotero_mcp/client.py`, `src/zotero_mcp/local_db.py`, `src/zotero_mcp/pdf_utils.py`
- Current high-risk areas from validation:
  - timeout-prone large-library paths
  - high-token default response payloads
  - parameter/schema ambiguity in some tool handlers

## Components
- Tool handlers: per-tool functions registered via `@mcp.tool` in `src/zotero_mcp/server.py`
- Local vs web behavior switches:
  - local API mode for local libraries
  - web API mode for broader write operations
- Output formatting layer: markdown-centric responses currently returned directly from tool handlers

## Patterns
- Use disposable `MCP_TEST_*` fixtures for write-path validation and cleanup.
- Prefer dry-run modes before batch mutations.
- For production hardening, enforce explicit response shaping defaults (`summary` + opt-in full content).
- For collection item lookups, fail fast on missing collection keys and avoid downstream list calls that can return misleading data.
- For ChatGPT connector compatibility, prefer `streamable-http` transport and place a stable HTTPS tunnel/proxy in front of local `127.0.0.1` service endpoints.
- For Windows laptop operations, keep startup/health automation in `scripts/windows/` and document end-to-end runbook steps in `docs/`.

## Recent Changes
- 2026-02-21: Fixed `zotero_get_collection_items` not-found handling in `src/zotero_mcp/server.py`.
- 2026-02-21: Added regression test `tests/test_server_collections.py` to ensure missing collections return explicit errors and do not call `collection_items`.
- 2026-02-22: Updated `zotero_advanced_search` in `src/zotero_mcp/server.py` to accept `operator` as an alias for `operation`.
- 2026-02-22: Extended `tests/test_server_advanced_search.py` with alias regression coverage and verified passing targeted tests.
- 2026-02-25: Added Windows ChatGPT HTTPS runbook `docs/chatgpt-windows-local-https.md` with streamable HTTP transport guidance, tunnel setup, validation checks, and Task Scheduler startup guidance.
- 2026-02-25: Added helper scripts for Windows operations: `scripts/windows/preflight-repo-hygiene.cmd`, `scripts/windows/start-zotero-mcp-http.cmd`, `scripts/windows/start-cloudflared-tunnel.cmd`, `scripts/windows/start-ngrok-tunnel.cmd`, and `scripts/windows/healthcheck-zotero-mcp.cmd`.
- 2026-02-25: Updated ChatGPT documentation in `docs/getting-started.md` and linked new Windows runbook in `README.md`.

## User Defined Namespaces
- [Leave blank - user populates]
