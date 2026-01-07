from unittest.mock import MagicMock, patch
import pytest
from zotero_mcp.server import (
    create_book,
    create_article,
    create_webpage,
    create_item,
    update_item,
    trash_item,
    delete_item_permanently,
    parse_creators
)
from fastmcp import Context

# Mock Context
@pytest.fixture
def mock_ctx():
    ctx = MagicMock(spec=Context)
    ctx.info = MagicMock()
    ctx.error = MagicMock()
    ctx.warn = MagicMock()
    return ctx

# Mock get_zotero_client
@pytest.fixture
def mock_zotero(mocker):
    mock_client = MagicMock()
    mocker.patch("zotero_mcp.server.get_zotero_client", return_value=mock_client)
    return mock_client

def test_parse_creators():
    assert parse_creators(["Smith, John"], "author") == [{"creatorType": "author", "lastName": "Smith", "firstName": "John"}]
    assert parse_creators(["Jane Doe"], "editor") == [{"creatorType": "editor", "lastName": "Doe", "firstName": "Jane"}]
    assert parse_creators(["SingleName"], "author") == [{"creatorType": "author", "name": "SingleName"}]

def test_create_book(mock_zotero, mock_ctx):
    # Setup mock
    mock_zotero.item_template.return_value = {
        "itemType": "book",
        "title": "",
        "date": "",
        "creators": [],
        "tags": [],
        "collections": []
    }
    mock_zotero.create_items.return_value = {"success": {"0": "NEWKEY123"}}

    # Call function via .fn to bypass FastMCP wrapper
    result = create_book.fn(
        title="My Book",
        authors=["Author, One"],
        date="2023",
        ctx=mock_ctx
    )

    # Assertions
    assert "NEWKEY123" in result
    mock_zotero.create_items.assert_called_once()
    call_args = mock_zotero.create_items.call_args[0][0]
    assert call_args[0]["title"] == "My Book"
    assert call_args[0]["date"] == "2023"
    assert call_args[0]["creators"][0]["firstName"] == "One"

def test_update_item(mock_zotero, mock_ctx):
    # Setup mock
    mock_item = {"key": "KEY123", "version": 1, "data": {"title": "Old Title"}}
    mock_zotero.item.return_value = mock_item
    mock_zotero.update_item.return_value = None

    # Call function
    result = update_item.fn(
        item_key="KEY123",
        item_data={"title": "New Title"},
        ctx=mock_ctx
    )

    # Assertions
    assert "Successfully updated" in result
    mock_zotero.item.assert_called_with("KEY123")
    mock_zotero.update_item.assert_called_once()
    assert mock_item["data"]["title"] == "New Title"

def test_trash_item(mock_zotero, mock_ctx):
    # Setup mock
    mock_item = {"key": "KEY123", "data": {"deleted": 0}}
    mock_zotero.item.return_value = mock_item

    # Call function
    result = trash_item.fn("KEY123", ctx=mock_ctx)

    # Assertions
    assert "trash" in result
    assert mock_item["data"]["deleted"] == 1
    mock_zotero.update_item.assert_called_once_with(mock_item)

def test_delete_permanently(mock_zotero, mock_ctx):
    # Setup mock
    mock_item = {"key": "KEY123", "version": 1}
    mock_zotero.item.return_value = mock_item

    # Call function
    result = delete_item_permanently.fn("KEY123", ctx=mock_ctx)

    # Assertions
    assert "permanently deleted" in result
    mock_zotero.delete_item.assert_called_once_with(mock_item)
