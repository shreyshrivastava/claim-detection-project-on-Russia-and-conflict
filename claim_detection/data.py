"""Loading helpers for JSONL evidence and evaluation fixtures."""

from __future__ import annotations

import json
from pathlib import Path

from claim_detection.config import DEFAULT_EVIDENCE_PATH
from claim_detection.schemas import EvidenceDocument


def load_evidence_jsonl(path: str | Path) -> list[EvidenceDocument]:
    documents: list[EvidenceDocument] = []
    for line_number, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        payload = json.loads(line)
        try:
            documents.append(
                EvidenceDocument(
                    id=str(payload["id"]),
                    title=str(payload["title"]),
                    text=str(payload["text"]),
                    source=str(payload.get("source", "fixture")),
                    published_at=payload.get("published_at"),
                )
            )
        except KeyError as exc:
            raise ValueError(f"Missing required field {exc} on line {line_number}") from exc
    return documents


def load_default_evidence() -> list[EvidenceDocument]:
    return load_evidence_jsonl(DEFAULT_EVIDENCE_PATH)
