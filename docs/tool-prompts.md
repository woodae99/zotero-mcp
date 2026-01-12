# MCP Tool Prompts

Use the prompts below with a local LLM to exercise each tool. Replace placeholders like `<ITEM_KEY>` as needed.

| Tool | Prompt | Notes |
| --- | --- | --- |
| zotero_search_items | Search my Zotero library for the phrase "MCP Seed" and return up to 5 results. |  |
| zotero_search_by_tag | Find items tagged with `mcp-seed-5a37b850` and return 5 results. | Tag must exist. |
| zotero_advanced_search | Run an advanced search: title contains "MCP Seed" AND item type is book; return up to 5 results. | Uses multi-condition search. |
| zotero_get_collections | List all collections in my Zotero library. |  |
| zotero_get_collection_items | List items in collection `<COLLECTION_KEY>` (limit 5). | Replace `<COLLECTION_KEY>`. |
| zotero_get_tags | List the first 10 tags in my library. |  |
| zotero_get_recent | Show my 5 most recently added items. |  |
| zotero_get_item_metadata | Show detailed metadata for item `<ITEM_KEY>` in markdown. | Replace `<ITEM_KEY>`. |
| zotero_get_item_metadata | Return BibTeX for item `<ITEM_KEY>`. | Pass `format="bibtex"` if needed. |
| zotero_get_item_fulltext | Get full text for item `<ITEM_KEY>`. | Attachments required for full text. |
| zotero_get_item_children | List child items (attachments/notes) for item `<ITEM_KEY>`. | Replace `<ITEM_KEY>`. |
| zotero_get_annotations | Get annotations for item `<ITEM_KEY>`. | Requires annotations or attachments. |
| zotero_get_notes | List 5 notes from my Zotero library. |  |
| zotero_search_notes | Search notes for the string "token" and return up to 5 results. |  |
| zotero_create_note | Create a note on item `<ITEM_KEY>` with text "# Test Note\n\nThis is a test note." and tag `mcp-note-test`. | Replace `<ITEM_KEY>`. |
| zotero_create_items | Create two items: a book titled "LLM Test Book" and a journal article titled "LLM Test Article", each with tag `mcp-write-test`. | Creates new items. |
| zotero_update_item | Update item `<ITEM_KEY>` to add tag `mcp-updated`. | Replace `<ITEM_KEY>`. |
| zotero_update_items | Batch update items `<ITEM_KEY_1>` and `<ITEM_KEY_2>` to set tag `mcp-batch-updated`. | Replace keys. |
| zotero_delete_item | Delete item `<ITEM_KEY>`. | Replace `<ITEM_KEY>`. |
| zotero_delete_items | Delete items `<ITEM_KEY_1>` and `<ITEM_KEY_2>`. | Replace keys. |
| zotero_create_collection | Create a collection named "LLM Test Collection". | Creates new collection. |
| zotero_update_collection | Rename collection `<COLLECTION_KEY>` to "LLM Test Collection Renamed". | Replace `<COLLECTION_KEY>`. |
| zotero_delete_collection | Delete collection `<COLLECTION_KEY>`. | Replace `<COLLECTION_KEY>`. |
| zotero_delete_collections | Delete collections `<COLLECTION_KEY_1>` and `<COLLECTION_KEY_2>`. | Replace keys. |
| zotero_create_saved_search | Create a saved search named "LLM Test Search" for title contains "MCP Seed". | Returns a search key. |
| zotero_delete_saved_search | Delete saved search `<SEARCH_KEY>`. | Replace `<SEARCH_KEY>`. |
| zotero_delete_tags | Delete tags `mcp-write-test`, `mcp-updated`, and `mcp-batch-updated`. | Tags must exist. |
| zotero_normalize_tags | Normalize tags for items matching "MCP Seed" to lowercase, trimming whitespace, dry run only. | `dry_run=true` recommended. |
| zotero_normalize_tags | Normalize tags for items matching "MCP Seed" to lowercase and apply changes (limit 5). | `dry_run=false`. |
| zotero_batch_update_items | Add tag `needs-abstract` to items where `abstractNote` is empty (limit 5, dry_run=false). | Uses advanced conditions. |
| zotero_collect_items | Add items matching "needs-abstract" to collection `<COLLECTION_KEY>` (limit 5, dry_run=false). | Replace `<COLLECTION_KEY>`. |
| zotero_plan_tag_normalization | Plan tag normalization for query "tag:ML" mapping "Machine Learning" -> "ML", case_mode=title, limit 200. | Returns a job id. |
| zotero_apply_tag_normalization | Apply tag normalization job `<JOB_ID>` with batch_size=50. | Replace `<JOB_ID>`. |
| zotero_resume_tag_normalization | Resume tag normalization job `<JOB_ID>` with batch_size=50. | Replace `<JOB_ID>`. |
| zotero_semantic_search | Semantic search for "graph neural networks" (limit 5). | Requires semantic search setup. |
| zotero_update_search_database | Update semantic search database (force_rebuild=false). | Requires semantic search setup. |
| zotero_get_search_database_status | Show semantic search database status. | Requires semantic search setup. |
| search | Search for "MCP Seed" using the connector search wrapper. | Connector wrapper. |
| fetch | Fetch item `<ITEM_KEY>` using the connector fetch wrapper. | Replace `<ITEM_KEY>`. |
