"""End-to-end claim analysis pipeline."""

from __future__ import annotations

from claim_detection.claim_detector import score_claim
from claim_detection.evidence import rank_evidence
from claim_detection.schemas import ClaimAnalysis, EvidenceDocument

LIMITATIONS = [
    "Deterministic screening output only; not a professional fact-check.",
    "Evidence stance is based on lexical and marker features, not verified ground truth.",
    "Live RSS feeds can change over time, so reproducible evaluation uses synthetic fixtures.",
]


def analyze_claim(
    claim: str,
    documents: list[EvidenceDocument],
    *,
    top_k: int = 3,
) -> ClaimAnalysis:
    """Analyze a claim against candidate evidence documents."""

    signal = score_claim(claim)
    evidence = rank_evidence(claim, documents, top_k=top_k)

    if not signal.is_claim:
        verdict = "not_a_clear_claim"
        confidence = round(max(0.0, 1 - signal.claim_score), 4)
    elif not evidence:
        verdict = "insufficient_evidence"
        confidence = 0.0
    else:
        top = evidence[0]
        verdict = top.stance
        confidence = round(min(1.0, (top.similarity * 0.7) + (top.overlap_ratio * 0.3)), 4)

    return ClaimAnalysis(
        claim=claim,
        signal=signal,
        verdict=verdict,
        confidence=confidence,
        evidence=evidence,
        limitations=LIMITATIONS,
    )
