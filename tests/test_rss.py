import sys
from types import SimpleNamespace

import pytest

from claim_detection.rss import fetch_rss_documents


def test_fetch_rss_documents_rejects_invalid_limit() -> None:
    with pytest.raises(ValueError, match="positive"):
        fetch_rss_documents(["https://example.com/feed.xml"], max_entries_per_feed=0)


def test_fetch_rss_documents_uses_feedparser_without_network(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_entry = SimpleNamespace(
        title=" Report title ",
        summary=" Summary body ",
        link="https://example.com/article",
        published="2026-07-24",
    )
    fake_feedparser = SimpleNamespace(parse=lambda _url: SimpleNamespace(entries=[fake_entry]))
    monkeypatch.setitem(sys.modules, "feedparser", fake_feedparser)

    documents = fetch_rss_documents(["https://example.com/feed.xml"], max_entries_per_feed=1)

    assert len(documents) == 1
    assert documents[0].title == "Report title"
    assert documents[0].source == "https://example.com/article"
