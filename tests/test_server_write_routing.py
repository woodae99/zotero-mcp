from zotero_mcp import server


class DummyContext:
    def info(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None

    def warn(self, *_args, **_kwargs):
        return None


class FakeLocalWriteClient:
    endpoint = "http://localhost:23119/api"
    local = True


class FakeWebWriteClient:
    endpoint = "https://api.zotero.org"
    local = False

    def __init__(self):
        self.updated_payload = None

    def item(self, _key):
        return {"data": {"key": "6IKHM6RA", "version": 1, "title": "Original"}}

    def update_item(self, payload):
        self.updated_payload = payload
        return True


def test_update_item_rejects_local_write_client(monkeypatch):
    monkeypatch.setattr(server, "get_zotero_client", lambda **_kw: FakeLocalWriteClient())

    result = server.update_item(
        item_key="6IKHM6RA",
        updates={"date": "2026"},
        ctx=DummyContext(),
    )

    assert "must use the Zotero web API endpoint" in result


def test_update_item_uses_web_write_client(monkeypatch):
    fake = FakeWebWriteClient()
    monkeypatch.setattr(server, "get_zotero_client", lambda **_kw: fake)

    result = server.update_item(
        item_key="6IKHM6RA",
        updates={"date": "2026"},
        ctx=DummyContext(),
    )

    assert "Updated item 6IKHM6RA: True" in result
    assert fake.updated_payload["date"] == "2026"
