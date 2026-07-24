"""Optional RSS ingestion helpers."""

from __future__ import annotations

from collections.abc import Iterable

from claim_detection.preprocessing import normalize_text
from claim_detection.schemas import EvidenceDocument


def fetch_rss_documents(
    feed_urls: Iterable[str], *, max_entries_per_feed: int = 5
) -> list[EvidenceDocument]:
    """Fetch RSS entries as evidence documents.

    This function is intentionally optional and is not used in CI evaluation.
    """

    if max_entries_per_feed < 1:
        raise ValueError("max_entries_per_feed must be positive")

    try:
        import feedparser
    except ImportError as exc:
        raise RuntimeError("Install feedparser to use RSS ingestion") from exc

    documents: list[EvidenceDocument] = []
    for feed_url in feed_urls:
        try:
            parsed = feedparser.parse(feed_url)
            # Some feeds might return parsed error responses/empty list of entries
            if not getattr(parsed, "entries", None):
                continue
            for index, entry in enumerate(parsed.entries[:max_entries_per_feed]):
                title = normalize_text(getattr(entry, "title", "Untitled RSS entry"))
                summary = normalize_text(getattr(entry, "summary", ""))
                link = getattr(entry, "link", feed_url)
                documents.append(
                    EvidenceDocument(
                        id=f"{feed_url}#{index}",
                        title=title,
                        text=summary,
                        source=link,
                        published_at=getattr(entry, "published", None),
                    )
                )
        except Exception:
            # Silently skip feed failures for robustness
            continue
    return documents
