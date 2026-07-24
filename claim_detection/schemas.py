"""Shared data structures for claim analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class EvidenceDocument:
    id: str
    title: str
    text: str
    source: str = "synthetic"
    published_at: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


@dataclass(frozen=True)
class ClaimSignal:
    is_claim: bool
    claim_score: float
    features: dict[str, float | int]
    rationale: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceMatch:
    document: EvidenceDocument
    similarity: float
    overlap_ratio: float
    stance: str
    rationale: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "document": self.document.to_dict(),
            "similarity": self.similarity,
            "overlap_ratio": self.overlap_ratio,
            "stance": self.stance,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class ClaimAnalysis:
    claim: str
    signal: ClaimSignal
    verdict: str
    confidence: float
    evidence: list[EvidenceMatch]
    limitations: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "claim": self.claim,
            "signal": self.signal.to_dict(),
            "verdict": self.verdict,
            "confidence": self.confidence,
            "evidence": [match.to_dict() for match in self.evidence],
            "limitations": self.limitations,
        }
