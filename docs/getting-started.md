# Getting Started with Zotero MCP

This guide will walk you through the setup and basic usage of the Zotero MCP server, which allows AI assistants like Claude to interact with your Zotero library.

## Installation

First, install the Zotero MCP server using pip:

```bash
pip install zotero-mcp-server
```

## Configuration

The server needs to know how to connect to your Zotero library. There are two main ways to do this:

### Option 1: Local Zotero (Recommended)

If you're running Zotero 7 or newer on the same machine, you can connect to the local API:

1. Enable the local API in Zotero's preferences:
   - Open Zotero
   - Go to Edit > Preferences > Advanced > API
   - Check "Enable local API"

2. Set the environment variable:
   ```bash
   export ZOTERO_LOCAL=true
   ```

### Option 2: Zotero Web API

If you want to connect to your Zotero library via the web API:

1. Get your Zotero API key:
   - Go to [https://www.zotero.org/settings/keys](https://www.zotero.org/settings/keys)
   - Create a new key with appropriate permissions (at least "Read" access)

2. Find your library ID:
   - For personal libraries, your user ID is available at the same page
   - For group libraries, it's the number in the URL when viewing the group

3. Set the environment variables:
   ```bash
   export ZOTERO_API_KEY=your_api_key
   export ZOTERO_LIBRARY_ID=your_library_id
   export ZOTERO_LIBRARY_TYPE=user  # or 'group' for group libraries
   ```

## Integrating with Claude Desktop

To use Zotero MCP with Claude Desktop:

1. Make sure you have Claude Desktop installed
2. Open your Claude Desktop configuration:
   - On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

3. Add the Zotero MCP server to the configuration:
   ```json
   {
     "mcpServers": {
       "zotero": {
         "command": "zotero-mcp",
         "env": {
           "ZOTERO_LOCAL": "true"
         }
       }
     }
   }
   ```

4. Restart Claude Desktop

- The tool should be available automatically: if not, you might need to double check in the connections menu under Settings.

## Integrating with OpenAI ChatGPT (Developer Mode)

ChatGPT custom MCP connectors require an HTTPS-reachable MCP endpoint. A practical setup is to run `zotero-mcp` locally on your laptop and expose it through an HTTPS tunnel/proxy.

Use `streamable-http` for new setups:

```bash
zotero-mcp serve --transport streamable-http --host 127.0.0.1 --port 8000
```

Then create an HTTPS tunnel endpoint (for example, Cloudflare Tunnel or ngrok with a reserved domain) that forwards traffic to `127.0.0.1:8000`.

In ChatGPT Developer Mode:

1. Open **Settings -> Connectors -> Create**.
2. Set the MCP URL to your HTTPS endpoint.
3. Select **No authentication** for this setup.
4. Save and verify that tools are discovered.

For a full Windows travel-laptop runbook (startup, tunnel stability, validation, and recovery), see [ChatGPT Desktop (Windows) Local HTTPS guide](./chatgpt-windows-local-https.md).

## Integrating with Chorus.sh

[Chorus.sh](https://chorus.sh) is a popular multi-chatbot interface that configures MCP servers through an online preferences form rather than config files.
This would be one possible path to working with Zotero with chatbots other than Claude.

To set up Zotero MCP with Chorus.sh:

1. **Find your installation path**:
   - For uv: typically `/Users/USERNAME/.pyenv/versions/3.12.8/bin/zotero-mcp` on macOS
   - For other methods: use `zotero-mcp setup-info` to get the exact path and configuration details

2. **Configure in Chorus.sh preferences**:
   - **Command**: Enter the full path to your zotero-mcp installation
   - **Arguments**: Leave empty (no custom --port or --host arguments needed unless set at config time)
   - **Environment (JSON)**: Take your environment configuration JSON (including outer brackets), remove newlines, and paste as a single line

3. **Example Environment JSON** (single line format):
   ```json
   {"ZOTERO_LOCAL": "true"}
   ```

Many other MCP consumers use similar configuration approaches with command path, arguments, and environment variables.

## Using with Other MCP Clients

Zotero MCP works with any MCP-compatible client. You can start the server manually:

```bash
zotero-mcp serve --transport stdio
```

For HTTP-based clients:

```bash
zotero-mcp serve --transport streamable-http --host localhost --port 8000
```


## Available Tools

### Read & Search Tools

When connected to Claude Desktop or another MCP client, you'll have access to these tools:

- **zotero_search_items**: Search your library by title, creator, or content
- **zotero_search_by_tag**: Find items by tag with AND/OR/NOT logic
- **zotero_advanced_search**: Multi-field search with conditions
- **zotero_search_notes**: Search note content and PDF annotations
- **zotero_get_item_metadata**: Get detailed information about a specific item
- **zotero_get_item_fulltext**: Get the full text content of an item
- **zotero_get_collections**: List all collections in your library
- **zotero_get_collection_items**: Get all items in a specific collection
- **zotero_get_item_children**: Get child items (attachments, notes) for a specific item
- **zotero_get_tags**: Get all tags used in your library
- **zotero_get_recent**: Get recently added items to your library
- **zotero_get_annotations**: Get PDF/EPUB annotations for an item
- **zotero_get_notes**: Get notes attached to an item
- **zotero_get_capabilities**: Inspect whether the current MCP session has local reads, web-write credentials, and any special routing exceptions
- **zotero_list_libraries**: List accessible Zotero libraries
- **zotero_list_feeds**: List RSS/Atom feeds in your library
- **zotero_get_feed_items**: Get items from a feed

### Write & Management Tools

These tools require the Zotero **web API** (`ZOTERO_API_KEY` + `ZOTERO_LIBRARY_ID`). The local
API (Zotero 7 running on your machine) supports reads only. In a **hybrid setup** — where you
set `ZOTERO_LOCAL=true` for fast local reads but also supply web credentials — these tools
automatically route writes through the web API.

> **Hybrid mode** (recommended for large libraries): set `ZOTERO_LOCAL=true` AND provide
> `ZOTERO_API_KEY` / `ZOTERO_LIBRARY_ID`. Reads use the local instance; writes use the web API.

#### Item management
- **zotero_create_items**: Add new items to the library (books, articles, web pages, etc.)
- **zotero_update_item**: Update a single item's metadata (PATCH semantics — only supplied fields change)
- **zotero_delete_item**: Delete one or more items (accepts a single key or a list)

#### Notes
- `zotero_create_note` can write in local mode via Zotero's connector `saveItems` endpoint.
- `zotero_create_annotation` still performs the write step via the Zotero web API.
- **zotero_create_note**: Create a note attached to an item — ideal for summaries, reviews, or extracted insights
- **zotero_create_annotation**: Create a highlight annotation on a PDF or EPUB

#### Collection management
- **zotero_create_collection**: Create a new collection (folder)
- **zotero_update_collection**: Rename a collection or change its parent
- **zotero_delete_collection**: Delete one or more collections (items inside are not deleted)

#### Tag management
- **zotero_batch_update_tags**: Add or remove tags across all items matching a search query
- **zotero_normalize_tags**: Standardise tag casing, whitespace, or rename tags via a mapping. Run with `dry_run=true` first to preview.
- **zotero_delete_tags**: Remove a tag from the entire library

#### Batch operations
- **zotero_batch_update_items**: Apply a field update to all items matching a search query. Always preview with `dry_run=true` first.
- **zotero_collect_items**: Add all items matching a search query to a collection

## Example Queries

Once connected, you can ask Claude questions like:

**Reading & searching**
- "Search my Zotero library for papers about machine learning"
- "Find articles by Smith in my Zotero library"
- "Show me my most recent additions to Zotero"
- "What collections do I have in my Zotero library?"
- "Get the full text of paper XYZ from my Zotero library"

**Librarian tasks** *(require web API)*
- "Add this paper to my Zotero library: [title, authors, DOI]"
- "Summarise the full text of paper XYZ and save the summary as a note"
- "Find all items tagged 'to-read' and add the tag 'reviewed'"
- "Show me all tags that are variations of 'machine learning' and normalise them"
- "Create a collection called 'Deep Learning 2024' and add all papers from 2024 about deep learning to it"
- "Delete the tags 'temp' and 'draft' from my library"

## Troubleshooting

If you encounter issues:

- Make sure Zotero is running (for local API)
- Check that your API key has the correct permissions
- Verify your library ID and type
- Look for error messages in the Claude Desktop logs or MCP server output

### Local Library Limitations

The local Zotero API (port 23119) is read-only — it does not support creating or modifying items,
collections, or tags. Write and management tools require the Zotero web API.

Exception: `zotero_create_note` can still create notes in local mode via Zotero's
local connector endpoint, while `zotero_create_annotation` continues to require
the web API for the write step.

**Recommended hybrid setup**: supply both local and web credentials. Reads are fast (local), and
writes are routed automatically to the web API:

```bash
export ZOTERO_LOCAL=true          # fast local reads
export ZOTERO_API_KEY=your_key    # enables write tools via web API
export ZOTERO_LIBRARY_ID=your_id
```

This gives you the best of both: low-latency reads for large libraries and full write access for
librarian and research-assistant tasks.

### Database Issues

Switching installs or install methods (sometimes to deal with failed installs), as well as toggling between search options, can sometimes lead to database problems. These can frequently be solved with:

```bash
zotero-mcp update-db --force-rebuild
```

Other than time waiting for the rebuild, there is generally little to no risk involved in triggering the rebuild - so if you're experiencing database-related issues, it's worth trying this command.

For more help, try the [discussions](https://github.com/54yyyu/zotero-mcp/discussions).
