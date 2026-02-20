## Overview
- Project: `zotero-mcp`
- Purpose: MCP server exposing Zotero read/write/fulltext/search tooling for AI agents.
- Core constraint: local Zotero API is best for local full-text/read speed, while reliable create/update/delete requires Zotero Web API credentials.

## Architecture
- MCP tools are registered in `src/zotero_mcp/server.py`.
- Zotero client creation/routing is centralized in `src/zotero_mcp/client.py`.
- CLI/setup configuration flows are in `src/zotero_mcp/cli.py` and `src/zotero_mcp/setup_helper.py`.

## Key Components
- `get_zotero_client(operation=...)` in `src/zotero_mcp/client.py`
  - `operation="read"`: local/web routing by mode.
  - `operation="fulltext"`: local-first for attachment/fulltext retrieval.
  - `operation="write"`: web-first when credentials exist.
- Setup writers in `src/zotero_mcp/setup_helper.py`
  - Persist both local + web vars for hybrid operation.
  - Persist `ZOTERO_READ_MODE` and `ZOTERO_WRITE_MODE`.

## Patterns
- Hybrid routing pattern:
  - `ZOTERO_LOCAL=true`
  - `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_ID`, `ZOTERO_LIBRARY_TYPE` set
  - `ZOTERO_READ_MODE=local`
  - `ZOTERO_WRITE_MODE=web`
- Tool-level routing in `server.py`:
  - Read tools call `get_zotero_client(operation="read")`.
  - Fulltext/fetch paths call `get_zotero_client(operation="fulltext")`.
  - Mutating tools call `get_zotero_client(operation="write")`.
- CLI output compatibility pattern:
  - Keep `src/zotero_mcp/cli.py` output ASCII-only to avoid Windows console encoding failures.
- Optional semantic tool exclusion pattern:
  - Set `ZOTERO_ENABLE_SEMANTIC_TOOLS=false` to hide semantic/db MCP tools.
  - Setup shortcut: `zotero-mcp setup --disable-semantic-tools` writes this flag into client config.
  - Upstream-safe default remains enabled (`true`), so existing behavior is unchanged for other users.
- Documentation anchors:
  - `README.md`: setup/advanced configuration + environment variable references.
  - `docs/getting-started.md`: mode selection and hybrid examples.
  - `docs/tool-prompts.md`: tool exercise prompts and write-tool prerequisites.

## User Defined Namespaces
- [Leave blank - user populates]
