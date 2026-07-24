"""Text normalization helpers."""

from __future__ import annotations

import re
import unicodedata

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
}


def normalize_text(text: str) -> str:
    """Normalize unicode, whitespace, and casing for deterministic NLP features."""

    normalized = unicodedata.normalize("NFKC", text or "")
    normalized = re.sub(r"https?://\S+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def split_sentences(text: str) -> list[str]:
    cleaned = normalize_text(text)
    if not cleaned:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def tokenize(text: str, *, remove_stopwords: bool = True) -> list[str]:
    tokens = re.findall(r"[a-z0-9][a-z0-9-]*", normalize_text(text).lower())
    if remove_stopwords:
        return [token for token in tokens if token not in STOPWORDS]
    return tokens
