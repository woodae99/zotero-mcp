from zotero_mcp import server


class DummyContext:
    def info(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None

    def warn(self, *_args, **_kwargs):
        return None


def test_get_capabilities_reports_local_read_and_web_write(monkeypatch):
    monkeypatch.setattr(server, "is_local_mode", lambda: True)
    monkeypatch.setattr(server, "get_local_zotero_client", lambda: object())
    monkeypatch.setattr(server, "get_web_zotero_client", lambda: object())
    monkeypatch.setattr(server, "get_active_library", lambda: {})
    monkeypatch.setenv("ZOTERO_LIBRARY_ID", "6377355")
    monkeypatch.setenv("ZOTERO_LIBRARY_TYPE", "user")
    monkeypatch.setenv("ZOTERO_LOCAL_PORT", "23119")

    result = server.get_capabilities(ctx=DummyContext())

    assert "Local read access available now: True" in result
    assert "Web write credentials configured: True" in result
    assert "zotero_create_note is the main exception" in result
    assert "zotero_create_annotation always writes via the web API" in result
    assert "Active library target: user:6377355" in result


def test_get_capabilities_reports_missing_web_write_and_override(monkeypatch):
    monkeypatch.setattr(server, "is_local_mode", lambda: False)
    monkeypatch.setattr(server, "get_local_zotero_client", lambda: None)
    monkeypatch.setattr(server, "get_web_zotero_client", lambda: None)
    monkeypatch.setattr(
        server,
        "get_active_library",
        lambda: {"library_id": "999", "library_type": "group"},
    )
    monkeypatch.delenv("ZOTERO_LIBRARY_ID", raising=False)
    monkeypatch.delenv("ZOTERO_LIBRARY_TYPE", raising=False)

    result = server.get_capabilities(ctx=DummyContext())

    assert "Read mode preference: web" in result
    assert "Web write credentials configured: False" in result
    assert "Runtime library override is active" in result
    assert "Active library target: group:999" in result
