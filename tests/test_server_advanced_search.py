from zotero_mcp import server


class DummyContext:
    def info(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None

    def warn(self, *_args, **_kwargs):
        return None


class FakeZotero:
    def __init__(self, items):
        self._items = items

    def saved_search(self, _name, _conditions):
        return {"success": {"0": "TEMPSEARCH01"}}

    def add_parameters(self, **_kwargs):
        return None

    def items(self):
        return self._items

    def delete_saved_search(self, _keys):
        return None


def test_advanced_search_accepts_operator_alias(monkeypatch):
    fake_items = [
        {
            "key": "AAA11111",
            "data": {
                "itemType": "journalArticle",
                "title": "Quantum Networks and Learning",
                "date": "2024",
                "creators": [{"firstName": "Jane", "lastName": "Doe"}],
                "tags": [{"tag": "physics"}],
            },
        }
    ]
    monkeypatch.setattr(server, "get_zotero_client", lambda *args, **kwargs: FakeZotero(fake_items))

    result = server.advanced_search(
        conditions=[{"field": "title", "operator": "contains", "value": "quantum"}],
        join_mode="all",
        limit=10,
        ctx=DummyContext(),
    )

    assert "Quantum Networks and Learning" in result
