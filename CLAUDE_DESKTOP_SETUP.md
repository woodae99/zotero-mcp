# Claude Desktop Configuration for Zotero MCP

## Windows Configuration (Your Setup)

### Step 1: Locate Configuration File
Claude Desktop config is stored at:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Full Path**: `C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json`

### Step 2: Open in Text Editor
1. Press `Windows Key + R`
2. Type: `%APPDATA%\Claude`
3. Press Enter
4. Find and open `claude_desktop_config.json` with your text editor (Notepad, VS Code, etc.)

### Step 3: Add Zotero MCP Server
**Basic Configuration (Recommended)**:
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

**Advanced Configuration (With environment variables)**:
```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "args": ["serve"],
      "env": {
        "ZOTERO_API_KEY": "YOUR_API_KEY",
        "ZOTERO_LIBRARY_ID": "YOUR_LIBRARY_ID",
        "ZOTERO_LIBRARY_TYPE": "user"
      }
    }
  }
}
```

**Using Local Zotero (Read-only)**:
```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "args": ["serve"],
      "env": {
        "ZOTERO_LOCAL": "true"
      }
    }
  }
}
```

### Step 4: Save and Exit
Save the file (Ctrl+S or File > Save)

### Step 5: Restart Claude Desktop
1. **Completely close** Claude Desktop (not just minimize)
2. Open Claude Desktop again
3. Wait 5-10 seconds for server to start
4. The Zotero tools should now be available

---

## Verifying the Integration

### Check in Claude Settings
1. Open Claude Desktop
2. Click **Settings** (gear icon)
3. Navigate to **Connections**
4. You should see "Zotero" listed as an active connection
5. If it shows as unavailable, check the error message

### Test in Chat
Once Zotero appears in your connections, try these messages in Claude:

```
Q: "Search my Zotero library for papers on machine learning"
Expected: Claude searches your library and returns results

Q: "Show me my Zotero collections"
Expected: List of all your collections

Q: "What are the recent items I added?"
Expected: List of recently added papers

Q: "Find papers similar to [topic]"
Expected: Semantic search results (if configured)
```

---

## Troubleshooting

### "Zotero connection unavailable" or won't connect

**Solution 1: Verify command is available**
```bash
# Open PowerShell and run:
where zotero-mcp

# If this shows a path, command is available
# If not found, add Python Scripts to PATH
```

**Solution 2: Check the config JSON syntax**
```bash
# Use an online JSON validator or:
# Open in VS Code (it highlights syntax errors)
```

**Solution 3: Run server manually to see errors**
```bash
# Open PowerShell and run:
zotero-mcp serve

# Watch for error messages. Common issues:
# - API key not set
# - Library ID incorrect
# - Network connection issues
```

**Solution 4: Restart everything**
```bash
# 1. Close Claude Desktop completely
# 2. Open PowerShell
# 3. Run: zotero-mcp serve
# 4. Keep that window open
# 5. Open Claude Desktop in another window
# 6. Try using Zotero tools
```

### "Command not found: zotero-mcp"

**Solution 1: Use full path**
```bash
# Find Python Scripts folder:
python -c "import site; print(site.USER_SITE)"

# Then in Claude config, use full path:
{
  "command": "C:\\Users\\YourName\\AppData\\Roaming\\Python\\Python313\\Scripts\\zotero-mcp.exe"
}
```

**Solution 2: Add to PATH**
```bash
# 1. Find Python Scripts folder (see above)
# 2. Open Settings > Environment Variables
# 3. Click "Edit environment variables"
# 4. Add Python Scripts folder to PATH
# 5. Restart Claude Desktop
```

### Connection works but no tools appear

**Solution:**
```bash
# 1. Check the server is actually running:
#    - Open a PowerShell window
#    - Run: zotero-mcp serve
#    - You should see: "Starting Zotero MCP server..."
# 
# 2. Make sure Claude config is saved (Ctrl+S)
#
# 3. Fully restart Claude Desktop (close all windows)
#
# 4. Wait 10+ seconds after opening Claude before trying to use tools
#
# 5. Check Connections in Settings to see if Zotero shows an error
```

### Tools appear but respond with errors

**Solution:**
```bash
# 1. Verify API credentials:
#    - Go to https://www.zotero.org/settings/keys
#    - Check your API key and library ID
#    - Make sure key has "read" permissions
#
# 2. Test connection directly:
#    python test_local_setup.py
#
# 3. Check the server terminal for error messages
#    (the PowerShell window where you ran zotero-mcp serve)
```

---

## Configuration Examples

### Example 1: Using Web API (Cloud Library)
```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "args": ["serve"],
      "env": {
        "ZOTERO_API_KEY": "YOUR_KEY_HERE",
        "ZOTERO_LIBRARY_ID": "YOUR_ID_HERE",
        "ZOTERO_LIBRARY_TYPE": "user"
      }
    }
  }
}
```

### Example 2: Using Local API (Offline)
```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "args": ["serve"],
      "env": {
        "ZOTERO_LOCAL": "true"
      }
    }
  }
}
```

### Example 3: Multiple Zotero Libraries
```json
{
  "mcpServers": {
    "zotero-main": {
      "command": "zotero-mcp",
      "args": ["serve"],
      "env": {
        "ZOTERO_API_KEY": "KEY_FOR_MAIN_LIBRARY",
        "ZOTERO_LIBRARY_ID": "12345",
        "ZOTERO_LIBRARY_TYPE": "user"
      }
    },
    "zotero-research": {
      "command": "zotero-mcp",
      "args": ["serve"],
      "env": {
        "ZOTERO_API_KEY": "KEY_FOR_RESEARCH_GROUP",
        "ZOTERO_LIBRARY_ID": "67890",
        "ZOTERO_LIBRARY_TYPE": "group"
      }
    }
  }
}
```

---

## Getting Your API Key & Library ID

### Step 1: Get API Key
1. Go to: https://www.zotero.org/settings/keys
2. Click "Create new private key"
3. Select permissions: at minimum "Read library"
4. Copy the key (looks like: `AbCdEfGhIjKlMnOpQrStUv`)

### Step 2: Get Library ID
**For Personal Library:**
1. Go to: https://www.zotero.org/settings/keys (same page)
2. Look for your **User ID** on the left side
3. That's your ZOTERO_LIBRARY_ID

**For Group Library:**
1. Go to your group page on Zotero
2. Look at the URL: `https://www.zotero.org/groups/123456/groupname`
3. The number (123456) is your ZOTERO_LIBRARY_ID
4. Use `ZOTERO_LIBRARY_TYPE: "group"` instead of "user"

---

## Using the Zotero Tools in Claude

Once connected, you can ask Claude to:

### Search Your Library
```
"Find papers about quantum computing in my Zotero library"
"Search my library for items tagged with 'machine-learning'"
"Show me all items by author Smith published after 2020"
```

### Get Information
```
"What collections do I have in Zotero?"
"Show me my recent Zotero additions"
"Get the abstract of paper with key ABC12345"
"Extract the full text from this PDF in my library"
```

### Manage Your Library
```
"Create a new collection called 'Active Research'"
"Add all papers about neural networks to my collection"
"Tag these items with 'review-needed'"
"Create a note on item XYZ12345"
```

### Advanced Features
```
"Find papers semantically similar to [description]"
"Extract all annotations from paper ABC"
"Show me papers matching these criteria: [criteria]"
"Normalize tags across my library"
```

---

## Advanced: Running as Background Service

If you want Zotero MCP to run automatically when Claude starts:

### Option 1: Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Zotero MCP"
4. Trigger: "At startup"
5. Action: Start a program
6. Program: `C:\Users\YourName\AppData\Local\Programs\Python\Python313\Scripts\zotero-mcp.exe`
7. Arguments: `serve`

### Option 2: Windows Startup Folder
1. Create a batch file `start-zotero-mcp.bat`:
```batch
@echo off
zotero-mcp serve
```
2. Place in: `C:\Users\YourName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

---

## Quick Troubleshooting Checklist

- [ ] Claude config file exists at `%APPDATA%\Claude\claude_desktop_config.json`
- [ ] Config has valid JSON (no syntax errors)
- [ ] Zotero server is in `mcpServers` section
- [ ] Claude Desktop fully restarted (not just closed)
- [ ] API key is set in `.env` or config `env` section
- [ ] Library ID is correct (from your Zotero settings)
- [ ] `zotero-mcp` command works in PowerShell
- [ ] Server shows "Starting Zotero MCP server..." when run manually
- [ ] Zotero appears in Claude Settings > Connections

If still having issues:
1. Run: `python test_local_setup.py`
2. Check the full error message
3. Review the solution for that specific error above

---

## Support

- **Server won't start**: Check terminal output when running `zotero-mcp serve`
- **API errors**: Verify credentials at https://www.zotero.org/settings/keys
- **Config issues**: Use https://jsonlint.com to validate JSON
- **General help**: See `LOCAL_TESTING_GUIDE.md` in the project

---

**Last Updated**: January 29, 2026  
**Status**: ✅ Ready for use
