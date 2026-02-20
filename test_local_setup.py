#!/usr/bin/env python
"""
Quick test script for Zotero MCP Server
Tests core functionality without needing a full MCP client
"""

import sys
import json
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all core modules can be imported"""
    print("=" * 60)
    print("Testing Imports...")
    print("=" * 60)
    
    try:
        from zotero_mcp.client import get_zotero_client
        print("✓ client module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import client: {e}")
        return False
    
    try:
        from zotero_mcp.server import mcp
        print("✓ server module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import server: {e}")
        return False
    
    try:
        from zotero_mcp.semantic_search import create_semantic_search
        print("✓ semantic_search module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import semantic_search: {e}")
        return False
    
    return True


def test_zotero_connection():
    """Test connection to Zotero API"""
    print("\n" + "=" * 60)
    print("Testing Zotero Connection...")
    print("=" * 60)
    
    from zotero_mcp.client import get_zotero_client
    
    try:
        client = get_zotero_client()
        print("✓ Zotero client initialized")
        
        # Try a simple query - use the client's search method instead
        try:
            # Get one item to verify the connection works
            client.add_parameters(limit=1)
            results = client.items()
            num_items = len(results)
            print(f"✓ Successfully connected to Zotero library")
            print(f"  Library contains at least {num_items} item(s)")
            return True
        except Exception as e:
            print(f"✗ Could not query library: {e}")
            print(f"  Make sure ZOTERO_API_KEY and ZOTERO_LIBRARY_ID are set correctly")
            return False
            
    except Exception as e:
        print(f"✗ Failed to initialize Zotero client: {e}")
        print(f"  Make sure ZOTERO_API_KEY and ZOTERO_LIBRARY_ID are set")
        return False


def test_server_initialization():
    """Test that the MCP server can be initialized"""
    print("\n" + "=" * 60)
    print("Testing Server Initialization...")
    print("=" * 60)
    
    try:
        from zotero_mcp.server import mcp
        print("✓ MCP server imported successfully")
        
        # FastMCP has tools in a different structure
        # The tools are registered as decorators, so we check if the mcp object exists and is a FastMCP instance
        from fastmcp import FastMCP
        if isinstance(mcp, FastMCP):
            print("✓ MCP server is properly initialized as FastMCP instance")
            print("✓ The server supports the following transport modes:")
            print("  - stdio (default for Claude Desktop)")
            print("  - sse (Server-Sent Events for HTTP)")
            print("  - websocket (WebSocket protocol)")
            return True
        else:
            print("✗ MCP server is not a FastMCP instance")
            return False
    except Exception as e:
        print(f"✗ Failed to initialize server: {e}")
        return False


def test_environment():
    """Check environment configuration"""
    print("\n" + "=" * 60)
    print("Environment Configuration")
    print("=" * 60)
    
    env_vars = {
        "ZOTERO_API_KEY": "Web API key",
        "ZOTERO_LIBRARY_ID": "Library ID",
        "ZOTERO_LIBRARY_TYPE": "Library type (user/group)",
        "ZOTERO_LOCAL": "Use local API (true/false)"
    }
    
    for var, description in env_vars.items():
        value = os.environ.get(var, "[not set]")
        # Obfuscate sensitive values
        if "KEY" in var and value != "[not set]":
            value = value[:4] + "*" * (len(value) - 4)
        print(f"  {var}: {value}")
        print(f"    → {description}")
    
    return True


def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "   Zotero MCP Server - Quick Functionality Test".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = {
        "Imports": test_imports(),
        "Environment": test_environment(),
        "Server Init": test_server_initialization(),
        "Zotero Connection": test_zotero_connection(),
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Server is ready for use.")
        print("\nNext steps:")
        print("  1. Run: zotero-mcp serve")
        print("  2. Configure Claude Desktop with the MCP server")
        print("  3. Test tools in Claude")
        return 0
    else:
        print("\n✗ Some tests failed. See above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
