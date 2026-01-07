from typing import List, Dict
import os

def format_creators(creators: list[dict[str, str]]) -> str:
    """
    Format creator names into a string.

    Args:
        creators: List of creator objects from Zotero.

    Returns:
        Formatted string with creator names.
    """
    names = []
    for creator in creators:
        if "firstName" in creator and "lastName" in creator:
            names.append(f"{creator['lastName']}, {creator['firstName']}")
        elif "name" in creator:
            names.append(creator["name"])
    return "; ".join(names) if names else "No authors listed"


def parse_creators(creators_list: list[str], creator_type: str = "author") -> list[dict[str, str]]:
    """
    Parse a list of creator names strings into Zotero creator objects.

    Args:
        creators_list: List of name strings (e.g. ["Smith, John", "Doe, Jane"])
        creator_type: The type of creator (author, editor, etc.)

    Returns:
        List of Zotero creator dictionaries.
    """
    creators = []
    for name in creators_list:
        name = name.strip()
        if "," in name:
            # Assume "Last, First" format
            parts = name.split(",", 1)
            creators.append({
                "creatorType": creator_type,
                "lastName": parts[0].strip(),
                "firstName": parts[1].strip()
            })
        elif " " in name:
            # Assume "First Last" format - naive split on last space
            parts = name.rsplit(" ", 1)
            creators.append({
                "creatorType": creator_type,
                "lastName": parts[1].strip(),
                "firstName": parts[0].strip()
            })
        else:
            # Single name
            creators.append({
                "creatorType": creator_type,
                "name": name
            })
    return creators


def is_local_mode() -> bool:
    """Return True if running in local mode.

    Local mode is enabled when environment variable `ZOTERO_LOCAL` is set to a
    truthy value ("true", "yes", or "1", case-insensitive).
    """
    value = os.getenv("ZOTERO_LOCAL", "")
    return value.lower() in {"true", "yes", "1"}
