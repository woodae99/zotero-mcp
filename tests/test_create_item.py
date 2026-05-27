"""Tests for manual item creation (zotero_create_item)."""

import json

from conftest import DummyContext, FakeZotero

from zotero_mcp import server


class FakeZoteroForCreate(FakeZotero):
    def item_template(self, item_type):
        if item_type == "notAType":
            raise Exception("Invalid item type")
        return super().item_template(item_type)

    def item_creator_types(self, item_type):
        if item_type == "bookSection":
            return [
                {"creatorType": "author"},
                {"creatorType": "editor"},
                {"creatorType": "translator"},
            ]
        if item_type == "webpage":
            return [{"creatorType": "author"}]
        return [{"creatorType": "author"}, {"creatorType": "editor"}]


def _patch_hybrid(monkeypatch, read_zot, write_zot=None):
    monkeypatch.setattr(
        "zotero_mcp.tools._helpers._get_write_client",
        lambda ctx: (read_zot, write_zot or read_zot),
    )


def _json_result(result):
    return json.loads(result)


class TestCreateItemHappyPath:
    def test_creates_book_section_with_manual_metadata(self, monkeypatch):
        fake = FakeZoteroForCreate()
        _patch_hybrid(monkeypatch, fake)

        result = server.create_item(
            item_type="bookSection",
            title="Does It Matter What the Coach Thinks?",
            creators=[
                {"creatorType": "author", "firstName": "Peter", "lastName": "Jackson"},
                {"creatorType": "editor", "firstName": "David B.", "lastName": "Drake"},
            ],
            book_title="The Philosophy and Practice of Coaching",
            date="2012",
            pages="73-109",
            publisher="Wiley",
            doi="10.1002/9781119207795",
            isbn="978-0-470-98721-6",
            citation_key="jacksonDoesItMatter2012",
            tags=["manual-entry", "book-section"],
            ctx=DummyContext(),
        )

        assert len(fake.created) == 1
        item = fake.created[0]
        assert item["itemType"] == "bookSection"
        assert item["title"] == "Does It Matter What the Coach Thinks?"
        assert item["bookTitle"] == "The Philosophy and Practice of Coaching"
        assert item["pages"] == "73-109"
        assert item["DOI"] == "10.1002/9781119207795"
        assert item["ISBN"] == "978-0-470-98721-6"
        assert "Citation Key: jacksonDoesItMatter2012" in item["extra"]
        assert [t["tag"] for t in item["tags"]] == ["manual-entry", "book-section"]

        payload = _json_result(result)
        assert payload["ok"] is True
        assert payload["item_key"] == "KEY0000"
        assert payload["zotero_uri"] == "zotero://select/library/items/KEY0000"
        assert payload["metadata"]["bookTitle"] == "The Philosophy and Practice of Coaching"

    def test_organisation_creator_uses_single_name_field(self, monkeypatch):
        fake = FakeZoteroForCreate()
        _patch_hybrid(monkeypatch, fake)

        server.create_item(
            item_type="webpage",
            title="Policy brief",
            creators=[{"creatorType": "author", "name": "World Health Organization"}],
            ctx=DummyContext(),
        )

        creator = fake.created[0]["creators"][0]
        assert creator == {"creatorType": "author", "name": "World Health Organization"}

    def test_hybrid_mode_uses_write_client(self, monkeypatch):
        read_zot = FakeZoteroForCreate()
        write_zot = FakeZoteroForCreate()
        _patch_hybrid(monkeypatch, read_zot, write_zot)

        server.create_item(
            item_type="journalArticle",
            title="Manual article",
            publication_title="Journal of Tests",
            ctx=DummyContext(),
        )

        assert len(write_zot.created) == 1
        assert len(read_zot.created) == 0


class TestCreateItemValidation:
    def test_dry_run_returns_payload_without_writing(self, monkeypatch):
        fake = FakeZoteroForCreate()
        _patch_hybrid(monkeypatch, fake)

        result = server.create_item(
            item_type="book",
            title="Preview Only",
            publisher="Test Press",
            dry_run=True,
            ctx=DummyContext(),
        )

        payload = _json_result(result)
        assert payload["dry_run"] is True
        assert payload["payload"]["publisher"] == "Test Press"
        assert fake.created == []

    def test_unknown_item_type_returns_error(self, monkeypatch):
        fake = FakeZoteroForCreate()
        _patch_hybrid(monkeypatch, fake)

        result = server.create_item(
            item_type="notAType",
            title="Bad Type",
            ctx=DummyContext(),
        )

        assert "unknown or unsupported" in result
        assert fake.created == []

    def test_invalid_creator_role_returns_error(self, monkeypatch):
        fake = FakeZoteroForCreate()
        _patch_hybrid(monkeypatch, fake)

        result = server.create_item(
            item_type="webpage",
            title="Bad Creator",
            creators=[{"creatorType": "editor", "firstName": "Ed", "lastName": "Wrong"}],
            ctx=DummyContext(),
        )

        assert "creatorType 'editor'" in result
        assert fake.created == []

    def test_invalid_field_is_skipped_with_warning(self, monkeypatch):
        fake = FakeZoteroForCreate()
        _patch_hybrid(monkeypatch, fake)

        result = server.create_item(
            item_type="book",
            title="A Book",
            issue="4",
            publisher="Test Press",
            ctx=DummyContext(),
        )

        item = fake.created[0]
        assert "issue" not in item
        assert item["publisher"] == "Test Press"
        payload = _json_result(result)
        assert "Skipped issue" in payload["warnings"][0]

    def test_title_required(self, monkeypatch):
        fake = FakeZoteroForCreate()
        _patch_hybrid(monkeypatch, fake)

        result = server.create_item(
            item_type="book",
            title="",
            ctx=DummyContext(),
        )

        assert "title is required" in result
        assert fake.created == []


class TestCreateItemCollectionsAndRelations:
    def test_collection_keys_and_names_are_accepted(self, monkeypatch):
        fake = FakeZoteroForCreate()
        fake._collections = [
            {"key": "COLL0001", "data": {"name": "Manual Entries"}},
        ]
        _patch_hybrid(monkeypatch, fake)

        result = server.create_item(
            item_type="journalArticle",
            title="Collection Test",
            collections=["ABCD1234", "Manual Entries"],
            ctx=DummyContext(),
        )

        item = fake.created[0]
        assert "ABCD1234" in item["collections"]
        assert "COLL0001" in item["collections"]
        payload = _json_result(result)
        assert {"input": "ABCD1234", "used": "ABCD1234", "match": "key"} in payload["collection_resolution"]
        assert {"input": "Manual Entries", "used": "COLL0001", "match": "name"} in payload["collection_resolution"]

    def test_unknown_collection_name_errors_before_create(self, monkeypatch):
        fake = FakeZoteroForCreate()
        fake._collections = []
        _patch_hybrid(monkeypatch, fake)

        result = server.create_item(
            item_type="journalArticle",
            title="Missing Collection",
            collections=["Not There"],
            ctx=DummyContext(),
        )

        assert "No collection found" in result
        assert fake.created == []

    def test_relations_are_written(self, monkeypatch):
        fake = FakeZoteroForCreate()
        _patch_hybrid(monkeypatch, fake)

        server.create_item(
            item_type="journalArticle",
            title="Related",
            relations={"dc:relation": ["http://zotero.org/users/123/items/PARENT01"]},
            ctx=DummyContext(),
        )

        assert fake.created[0]["relations"] == {
            "dc:relation": ["http://zotero.org/users/123/items/PARENT01"]
        }

    def test_local_only_mode_returns_error(self, monkeypatch):
        monkeypatch.setattr(
            "zotero_mcp.tools._helpers._get_write_client",
            lambda ctx: (_ for _ in ()).throw(
                ValueError(
                    "Cannot perform write operations in local-only mode. "
                    "Add ZOTERO_API_KEY and ZOTERO_LIBRARY_ID to enable hybrid mode."
                )
            ),
        )

        result = server.create_item(
            item_type="book",
            title="No write client",
            ctx=DummyContext(),
        )

        assert "local-only" in result
