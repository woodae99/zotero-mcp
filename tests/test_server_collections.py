from zotero_mcp import server


class DummyContext:
    def info(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None

    def warn(self, *_args, **_kwargs):
        return None


class FakeZoteroMissingCollection:
    def __init__(self):
        self.collection_items_called = False

    def collection(self, _collection_key):
        return None

    def collection_items(self, _collection_key, limit=50):
        self.collection_items_called = True
        return [{"key": "SHOULD_NOT_BE_RETURNED", "data": {"title": "Wrong"}}]


def test_get_collection_items_returns_not_found_for_missing_collection(monkeypatch):
    fake_zot = FakeZoteroMissingCollection()
    monkeypatch.setattr(server, "get_zotero_client", lambda *args, **kwargs: fake_zot)

    result = server.get_collection_items(
        collection_key="MISSING123",
        limit=5,
        ctx=DummyContext(),
    )

    assert result == "Error: No collection found with key: MISSING123"
    assert fake_zot.collection_items_called is False
