# Zotero MCP Server - Local Testing Guide

## ✅ Installation Status
The Zotero MCP server has been successfully installed in editable mode with all dependencies.

**Installed Version**: 0.1.2  
**Python Version**: 3.13.11  
**Installation Type**: Editable (pip install -e .)

---

## 🚀 Quick Start Testing

### Option 1: Serve via stdio (Standard Input/Output)
This is the default MCP transport for Claude Desktop and other clients.

```bash
# Navigate to the project directory
cd c:\Users\colin\Dev\GitHub\zotero-mcp

# Run the server with environment from .env file
zotero-mcp serve
```

The server will start listening for MCP protocol messages on stdin/stdout. You can test it by:
- Starting Claude Desktop with the MCP configuration
- Using any other MCP-compatible client

### Option 2: Serve via HTTP/SSE (for remote clients)
If you want to test with web-based clients or tunneling services:

```bash
zotero-mcp serve --transport sse --host 0.0.0.0 --port 8000
```

Then your MCP endpoint will be available at: `http://localhost:8000/sse`

### Option 3: Serve with WebSocket transport
```bash
zotero-mcp serve --transport websocket --host 0.0.0.0 --port 8000
```

---

## ⚙️ Configuration

### Environment Variables
The server loads configuration from these sources (in priority order):

1. **Standalone config** (~/.config/zotero-mcp/config.json)
2. **Claude Desktop config** (%APPDATA%\Claude\claude_desktop_config.json)
3. **.env file** in the project root

**Current .env configuration:**
```
ZOTERO_API_KEY=OS3AH2z9rcONdKxOSS9BvNiX
ZOTERO_LIBRARY_ID=6377355
ZOTERO_LIBRARY_TYPE=user
```

This uses the **Zotero Web API** for cloud library access. Write operations (create/update/delete) are supported.

### Alternative: Use Local Zotero API
To use a local Zotero installation (read-only):

```bash
# Set environment variable before running
set ZOTERO_LOCAL=true
zotero-mcp serve
```

---

## 🧪 Testing with Claude Desktop

### Step 1: Locate Claude Desktop Config
On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### Step 2: Add Zotero MCP Server
Edit the config file and add:

```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "args": ["serve"],
      "env": {
        "ZOTERO_API_KEY": "OS3AH2z9rcONdKxOSS9BvNiX",
        "ZOTERO_LIBRARY_ID": "6377355",
        "ZOTERO_LIBRARY_TYPE": "user"
      }
    }
  }
}
```

### Step 3: Restart Claude Desktop
Close and reopen Claude Desktop. The Zotero tools should now be available.

### Step 4: Test the Integration
In Claude, you can now:
- Search your library: "Find papers on machine learning"
- Get item details: "What's in my library about neural networks?"
- Perform semantic search: "Show me papers similar to [topic]"
- Extract annotations from PDFs

---

## 📊 Available Tools

The Zotero MCP server exposes the following tools:

### Core Search & Retrieval
- `search_library` - Search by title, author, or keywords
- `semantic_search` - AI-powered semantic search over your library
- `fetch_item` - Get detailed metadata for a specific item
- `get_item_pdf_text` - Extract text from PDF attachments
- `get_item_annotations` - Extract PDF annotations and notes

### Library Management
- `list_collections` - View your library collections
- `list_tags` - Browse all tags in your library
- `get_recent_items` - See recently added items

### BibTeX Export
- `generate_bibtex` - Export items as BibTeX

### Advanced Features
- `get_attachment_details` - Get attachment metadata
- `search_annotations` - Search across all annotations in your library

---

## 🔄 Semantic Search Setup (Optional)

Semantic search requires embeddings and a vector database. To enable it:

```bash
# Initialize semantic search
zotero-mcp setup
```

Follow the interactive prompts to choose your embedding model:
- **Default** (free, CPU-based)
- **OpenAI** (requires API key)
- **Gemini** (requires API key)

Then index your library:

```bash
zotero-mcp update-db
```

Check the status:

```bash
zotero-mcp db-status
```

---

## 🛠️ Troubleshooting

### Server won't start
```bash
# Verify credentials
zotero-mcp version

# Check config
zotero-mcp setup-info

# Look for errors
zotero-mcp serve
```

### "Connection refused" in Claude Desktop
- Make sure the zotero-mcp command is in your PATH
- Try restarting Claude Desktop completely
- Check if the server process is actually running

### Semantic search not working
```bash
# Check database status
zotero-mcp db-status

# Rebuild the database
zotero-mcp update-db --force
```

### API key issues
- Verify the API key from https://www.zotero.org/settings/keys
- Ensure the library ID matches your user ID or group ID
- Check that the API key has read (and write, if needed) permissions

---

## 🔐 Environment Setup for Production

For secure deployment:

1. **Use a .env file** (already set up):
   ```bash
   # Load from .env before running
   python -m dotenv run zotero-mcp serve
   ```

2. **Or use system environment variables**:
   ```bash
   set ZOTERO_API_KEY=your_key
   set ZOTERO_LIBRARY_ID=your_id
   zotero-mcp serve
   ```

3. **For Claude Desktop**, store credentials in the config file

---

## 📝 Testing Checklist

- [ ] Server starts successfully: `zotero-mcp serve`
- [ ] Can search library: Ask Claude "Search my Zotero library for..."
- [ ] Can fetch items: Ask Claude "Get details on [item name]"
- [ ] Can extract PDFs: Ask Claude "What are the annotations in [paper]?"
- [ ] Semantic search works (if configured): Ask Claude "Find papers about..."
- [ ] Collections visible: Ask Claude "Show me my Zotero collections"
- [ ] Can list tags: Ask Claude "What tags do I have?"

---

## 📚 Additional Resources

- **GitHub**: https://github.com/54yyyu/zotero-mcp
- **Documentation**: Check `/docs` folder in this project
- **Zotero Settings**: https://www.zotero.org/settings/keys

---

## 🚀 Next Steps

1. **Start the server**: Run `zotero-mcp serve`
2. **Configure Claude Desktop** with the config snippet above
3. **Test basic search functionality** by querying your library
4. **(Optional) Set up semantic search** for advanced queries
5. **Share feedback** or report issues on GitHub

Good luck! 🎉
