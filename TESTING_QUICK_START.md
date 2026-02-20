# Zotero MCP Server - Quick Reference & Testing Guide

## ✅ System Status
All components are **ready for testing**!

- ✓ Python 3.13.11 installed
- ✓ All dependencies installed
- ✓ Server modules validated
- ✓ Zotero API connection confirmed
- ✓ Configuration loaded successfully

---

## 🚀 Start Testing

### Method 1: Direct Server Start (Simplest)
```bash
# Open a terminal in the project directory
cd c:\Users\colin\Dev\GitHub\zotero-mcp

# Start the server with stdio transport (default for Claude Desktop)
zotero-mcp serve
```

You should see:
```
Starting Zotero MCP server...
[Listening for MCP protocol messages on stdin/stdout]
```

### Method 2: With HTTP for Web Clients
```bash
# Start with HTTP/SSE transport for web-based clients
zotero-mcp serve --transport sse --host 0.0.0.0 --port 8000
```

Access at: `http://localhost:8000/sse`

### Method 3: WebSocket Transport
```bash
zotero-mcp serve --transport websocket --host 0.0.0.0 --port 8000
```

---

## 🧪 Testing in Claude Desktop

### Step 1: Locate Configuration
On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### Step 2: Add Zotero Server
Add this to the `mcpServers` section:

```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "args": ["serve"]
    }
  }
}
```

### Step 3: Restart Claude Desktop
Close and reopen Claude. The Zotero tools should appear in the tools menu.

### Step 4: Test These Queries
```
- "Search my library for machine learning papers"
- "Show me recent items I added"
- "What are my Zotero collections?"
- "Get details on item with key ABC12345"
- "Find papers about neural networks"
```

---

## 🛠️ Common Commands

### View Server Help
```bash
zotero-mcp --help
```

### Check Configuration Info
```bash
zotero-mcp setup-info
```

### Run Tests
```bash
python test_local_setup.py
```

### Update Semantic Search Database
```bash
zotero-mcp update-db
```

### Check Database Status
```bash
zotero-mcp db-status
```

---

## 📊 Available Tools

The server exposes these main categories of tools:

### Search & Retrieval
- `zotero_search_items` - Full-text search
- `zotero_semantic_search` - AI-powered semantic search
- `zotero_search_by_tag` - Search by tags
- `zotero_advanced_search` - Advanced multi-criteria search
- `zotero_get_item_metadata` - Get item details
- `zotero_get_item_fulltext` - Extract PDF content
- `zotero_search_notes` - Search notes

### Library Management
- `zotero_get_collections` - List collections
- `zotero_get_collection_items` - Items in a collection
- `zotero_get_tags` - View all tags
- `zotero_get_recent` - Recently added items
- `zotero_get_annotations` - View annotations
- `zotero_get_notes` - View notes

### Create & Update (Web API only)
- `zotero_create_items` - Add new items
- `zotero_update_item` - Modify items
- `zotero_create_note` - Add notes
- `zotero_batch_update_tags` - Bulk tag updates
- `zotero_create_collection` - New collections
- `zotero_delete_item` - Remove items

### Semantic Search
- `zotero_semantic_search` - AI-powered search
- `zotero_update_search_database` - Index library
- `zotero_get_search_database_status` - Check index

---

## 🔧 Troubleshooting

### Server won't start
```bash
# Check if zotero-mcp is in PATH
where zotero-mcp

# Verify Python installation
python --version

# Test imports directly
python -c "from zotero_mcp.server import mcp; print('OK')"
```

### Connection errors in Claude
- Make sure server is running in a terminal
- Check Claude Desktop config syntax (valid JSON)
- Restart Claude Desktop after config changes
- Try `zotero-mcp serve` directly to see error messages

### API key issues
- Get key from: https://www.zotero.org/settings/keys
- Verify ZOTERO_LIBRARY_ID matches your user ID
- Check that API key has read permissions (write optional)

### No Zotero items found
- Verify API key and library ID are correct
- Make sure your Zotero account has items
- Check at https://www.zotero.org/yourname to see your library

---

## 📁 Project Structure
```
zotero-mcp/
├── src/zotero_mcp/
│   ├── server.py              # Main MCP server (100+ tools)
│   ├── client.py              # Zotero API client wrapper
│   ├── semantic_search.py      # Vector search module
│   ├── cli.py                 # Command-line interface
│   └── ... (other modules)
├── pyproject.toml             # Python project config
├── .env                       # Environment variables (API credentials)
├── LOCAL_TESTING_GUIDE.md     # Full testing documentation
└── test_local_setup.py        # Setup verification script
```

---

## 📚 Documentation
- **Full Setup Guide**: `docs/getting-started.md`
- **GitHub**: https://github.com/54yyyu/zotero-mcp
- **Zotero Settings**: https://www.zotero.org/settings/keys

---

## 🎯 Next Steps

1. **Start the server**: `zotero-mcp serve`
2. **Configure Claude Desktop** using the config above
3. **Restart Claude** and try the test queries
4. **Explore tools** through Claude's interface
5. **(Optional) Setup semantic search** for advanced queries

---

## ✨ Example Workflows

### Research Paper Analysis
```
"Find papers about transformers"
→ "Get the full text of the top result"
→ "Extract all annotations from that paper"
```

### Library Organization
```
"Search for items without tags"
→ "Add tag 'reviewed' to matching items"
→ "Show me collections with more than 5 items"
```

### Knowledge Management
```
"Create a note on item ABC12345"
→ "Find similar papers using semantic search"
→ "Add them to a new collection called 'Follow-up Reading'"
```

---

**Status**: ✅ Ready for local testing  
**Configuration**: ✅ Active  
**API Connection**: ✅ Verified  
**Test Script**: ✅ All tests passed

Good luck! 🎉
