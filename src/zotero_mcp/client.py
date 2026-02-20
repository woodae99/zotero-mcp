"""
Zotero client wrapper for MCP server.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from markitdown import MarkItDown
from pyzotero import zotero

from zotero_mcp.utils import format_creators

# Load environment variables
load_dotenv()


def _is_truthy(value: str | None) -> bool:
    """Parse common truthy environment variable values."""
    if value is None:
        return False
    return value.strip().lower() in {"true", "yes", "1", "on"}


def _web_config_available() -> bool:
    """Return True when required Web API configuration is present."""
    return bool(os.getenv("ZOTERO_LIBRARY_ID") and os.getenv("ZOTERO_API_KEY"))


def _create_local_client() -> zotero.Zotero:
    """Create a client bound to the local Zotero API."""
    library_type = os.getenv("ZOTERO_LIBRARY_TYPE", "user")
    library_id = os.getenv("ZOTERO_LOCAL_LIBRARY_ID") or os.getenv("ZOTERO_LIBRARY_ID") or "0"
    return zotero.Zotero(
        library_id=library_id,
        library_type=library_type,
        api_key=None,
        local=True,
    )


def _create_web_client() -> zotero.Zotero:
    """Create a client bound to Zotero Web API."""
    library_id = os.getenv("ZOTERO_LIBRARY_ID")
    library_type = os.getenv("ZOTERO_LIBRARY_TYPE", "user")
    api_key = os.getenv("ZOTERO_API_KEY")

    if not (library_id and api_key):
        raise ValueError(
            "Missing required web configuration. Set ZOTERO_LIBRARY_ID and ZOTERO_API_KEY."
        )

    return zotero.Zotero(
        library_id=library_id,
        library_type=library_type,
        api_key=api_key,
        local=False,
    )


def _resolve_client_mode(operation: Literal["read", "fulltext", "write"]) -> Literal["local", "web"]:
    """Resolve local vs web routing for an operation."""
    read_mode = (os.getenv("ZOTERO_READ_MODE", "auto") or "auto").strip().lower()
    write_mode = (os.getenv("ZOTERO_WRITE_MODE", "auto") or "auto").strip().lower()

    local_enabled = _is_truthy(os.getenv("ZOTERO_LOCAL"))
    web_available = _web_config_available()

    if operation in {"read", "fulltext"}:
        if read_mode == "local":
            return "local"
        if read_mode == "web":
            return "web"
        # auto: prefer local for speed/offline/fulltext when available
        if local_enabled:
            return "local"
        return "web"

    # write operation
    if write_mode == "web":
        return "web"
    if write_mode == "local":
        return "local"
    # auto: prefer web when credentials exist because local endpoint is read-only
    if web_available:
        return "web"
    if local_enabled:
        return "local"
    return "web"


@dataclass
class AttachmentDetails:
    """Details about a Zotero attachment."""

    key: str
    title: str
    filename: str
    content_type: str


def get_zotero_client(operation: Literal["read", "fulltext", "write"] = "read") -> zotero.Zotero:
    """
    Get an authenticated Zotero client using operation-aware routing.

    Routing:
    - Reads/fulltext default to local API when ZOTERO_LOCAL=true (or ZOTERO_READ_MODE=local)
    - Writes default to Web API when credentials are present (or ZOTERO_WRITE_MODE=web)
    - Both can be overridden with ZOTERO_READ_MODE / ZOTERO_WRITE_MODE (local|web|auto)

    Returns:
        A configured Zotero client instance.

    Raises:
        ValueError: If required environment variables are missing.
    """
    mode = _resolve_client_mode(operation)
    if mode == "local":
        return _create_local_client()
    return _create_web_client()


def format_item_metadata(item: dict[str, Any], include_abstract: bool = True) -> str:
    """
    Format a Zotero item's metadata as markdown.

    Args:
        item: A Zotero item dictionary.
        include_abstract: Whether to include the abstract in the output.

    Returns:
        Markdown-formatted metadata.
    """
    data = item.get("data", {})
    item_type = data.get("itemType", "unknown")

    # Basic information
    lines = [
        f"# {data.get('title', 'Untitled')}",
        f"**Type:** {item_type}",
        f"**Item Key:** {data.get('key')}",
    ]

    # Date
    if date := data.get("date"):
        lines.append(f"**Date:** {date}")

    # Authors/Creators
    if creators := data.get("creators", []):
        lines.append(f"**Authors:** {format_creators(creators)}")

    # Publication details based on item type
    if item_type == "journalArticle":
        if journal := data.get("publicationTitle"):
            journal_info = f"**Journal:** {journal}"
            if volume := data.get("volume"):
                journal_info += f", Volume {volume}"
            if issue := data.get("issue"):
                journal_info += f", Issue {issue}"
            if pages := data.get("pages"):
                journal_info += f", Pages {pages}"
            lines.append(journal_info)
    elif item_type == "book":
        if publisher := data.get("publisher"):
            book_info = f"**Publisher:** {publisher}"
            if place := data.get("place"):
                book_info += f", {place}"
            lines.append(book_info)

    # DOI and URL
    if doi := data.get("DOI"):
        lines.append(f"**DOI:** {doi}")
    if url := data.get("url"):
        lines.append(f"**URL:** {url}")

    # Tags
    if tags := data.get("tags"):
        tag_list = [f"`{tag['tag']}`" for tag in tags]
        if tag_list:
            lines.append(f"**Tags:** {' '.join(tag_list)}")

    # Abstract
    if include_abstract and (abstract := data.get("abstractNote")):
        lines.extend(["", "## Abstract", abstract])

    # Collections
    if collections := data.get("collections", []):
        if collections:
            lines.append(f"**Collections:** {len(collections)} collections")

    # Notes - this requires additional API calls, so we just indicate if there are notes
    if "meta" in item and item["meta"].get("numChildren", 0) > 0:
        lines.append(f"**Notes/Attachments:** {item['meta']['numChildren']}")

    return "\n\n".join(lines)


def generate_bibtex(item: dict[str, Any]) -> str:
    """
    Generate BibTeX format for a Zotero item.

    Args:
        item: Zotero item data

    Returns:
        BibTeX formatted string
    """
    data = item.get("data", {})
    item_key = data.get("key")

    # Try Better BibTeX first
    try:
        from zotero_mcp.better_bibtex_client import ZoteroBetterBibTexAPI
        bibtex = ZoteroBetterBibTexAPI()

        if bibtex.is_zotero_running():
            return bibtex.export_bibtex(item_key)

    except Exception:
        # Continue to fallback method if Better BibTeX fails
        pass

    # Fallback to basic BibTeX generation
    item_type = data.get("itemType", "misc")

    if item_type in ["attachment", "note"]:
        raise ValueError(f"Cannot export BibTeX for item type '{item_type}'")

    # Map Zotero item types to BibTeX types
    type_map = {
        "journalArticle": "article",
        "book": "book",
        "bookSection": "incollection",
        "conferencePaper": "inproceedings",
        "thesis": "phdthesis",
        "report": "techreport",
        "webpage": "misc",
        "manuscript": "unpublished"
    }

    # Create citation key
    creators = data.get("creators", [])
    author = ""
    if creators:
        first = creators[0]
        author = first.get("lastName", first.get("name", "").split()[-1] if first.get("name") else "").replace(" ", "")

    year = data.get("date", "")[:4] if data.get("date") else "nodate"
    cite_key = f"{author}{year}_{item_key}"

    # Build BibTeX entry
    bib_type = type_map.get(item_type, "misc")
    lines = [f"@{bib_type}{{{cite_key},"]

    # Add fields
    field_mappings = [
        ("title", "title"),
        ("publicationTitle", "journal"),
        ("volume", "volume"),
        ("issue", "number"),
        ("pages", "pages"),
        ("publisher", "publisher"),
        ("DOI", "doi"),
        ("url", "url"),
        ("abstractNote", "abstract")
    ]

    for zotero_field, bibtex_field in field_mappings:
        if value := data.get(zotero_field):
            # Escape special characters
            value = value.replace("{", "\\{").replace("}", "\\}")
            lines.append(f'  {bibtex_field} = {{{value}}},')

    # Add authors
    if creators:
        authors = []
        for creator in creators:
            if creator.get("creatorType") == "author":
                if "lastName" in creator and "firstName" in creator:
                    authors.append(f"{creator['lastName']}, {creator['firstName']}")
                elif "name" in creator:
                    authors.append(creator["name"])
        if authors:
            lines.append(f'  author = {{{" and ".join(authors)}}},')

    # Add year
    if year != "nodate":
        lines.append(f'  year = {{{year}}},')

    # Remove trailing comma from last field and close entry
    if lines[-1].endswith(','):
        lines[-1] = lines[-1][:-1]
    lines.append("}")

    return "\n".join(lines)


def get_attachment_details(
    zot: zotero.Zotero, item: dict[str, Any]
) -> AttachmentDetails | None:
    """
    Get attachment details for a Zotero item, finding the most relevant attachment.

    Args:
        zot: A Zotero client instance.
        item: A Zotero item dictionary.

    Returns:
        AttachmentDetails if found, None otherwise.
    """
    data = item.get("data", {})
    item_type = data.get("itemType")
    item_key = data.get("key")

    # Direct attachment
    if item_type == "attachment":
        return AttachmentDetails(
            key=item_key,
            title=data.get("title", "Untitled"),
            filename=data.get("filename", ""),
            content_type=data.get("contentType", ""),
        )

    # For regular items, look for child attachments
    try:
        children = zot.children(item_key)

        # Group attachments by content type
        pdfs = []
        htmls = []
        others = []

        for child in children:
            child_data = child.get("data", {})
            if child_data.get("itemType") == "attachment":
                content_type = child_data.get("contentType", "")
                filename = child_data.get("filename", "")
                title = child_data.get("title", "Untitled")
                key = child.get("key", "")

                # Use MD5 as proxy for size (longer MD5 usually means larger file)
                size_proxy = len(child_data.get("md5", ""))

                attachment = (key, title, filename, content_type, size_proxy)

                if content_type == "application/pdf":
                    pdfs.append(attachment)
                elif content_type.startswith("text/html"):
                    htmls.append(attachment)
                else:
                    others.append(attachment)

        # Return first match in priority order (PDF > HTML > other)
        # Sort each category by size (descending) to get largest/most complete file
        for category in [pdfs, htmls, others]:
            if category:
                category.sort(key=lambda x: x[4], reverse=True)
                key, title, filename, content_type, _ = category[0]
                return AttachmentDetails(
                    key=key,
                    title=title,
                    filename=filename,
                    content_type=content_type,
                )
    except Exception:
        pass

    return None


def convert_to_markdown(file_path: str | Path) -> str:
    """
    Convert a file to markdown using markitdown library.

    Args:
        file_path: Path to the file to convert.

    Returns:
        Markdown text.
    """
    try:
        md = MarkItDown()
        result = md.convert(str(file_path))
        return result.text_content
    except Exception as e:
        return f"Error converting file to markdown: {str(e)}"
