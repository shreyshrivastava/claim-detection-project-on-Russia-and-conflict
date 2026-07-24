"""Rule-based stance screening from claim/evidence text."""

from __future__ import annotations

from claim_detection.preprocessing import normalize_text, tokenize

REFUTE_MARKERS = {
    "denied",
    "false",
    "incorrect",
    "misleading",
    "no",
    "not",
    "refuted",
    "rejected",
    "unfounded",
}

SUPPORT_MARKERS = {
    "according",
    "announced",
    "confirmed",
    "delivered",
    "opened",
    "reported",
    "verified",
}


def classify_stance(
    claim: str,
    evidence: str,
    similarity: float,
    overlap_ratio: float,
) -> tuple[str, list[str]]:
    """Classify coarse evidence stance for the highest-ranked snippet."""

    claim_tokens = set(tokenize(claim))
    evidence_text = normalize_text(evidence).lower()
    evidence_tokens = set(tokenize(evidence, remove_stopwords=False))
    refute_hits = sorted(evidence_tokens & REFUTE_MARKERS)
    support_hits = sorted(evidence_tokens & SUPPORT_MARKERS)
    rationale: list[str] = []

    if similarity < 0.08 or overlap_ratio < 0.12:
        return "insufficient_evidence", ["low lexical similarity and low claim-token overlap"]

    if refute_hits and overlap_ratio >= 0.25:
        rationale.append(f"refutation markers found: {', '.join(refute_hits)}")
        return "refuted", rationale

    if support_hits and overlap_ratio >= 0.25:
        rationale.append(f"support markers found: {', '.join(support_hits)}")
        return "supported", rationale

    if claim_tokens and claim_tokens.issubset(set(tokenize(evidence))):
        return "supported", ["evidence contains all claim content tokens"]

    if "did not" in evidence_text and overlap_ratio >= 0.2:
        return "refuted", ["explicit negation phrase found in related evidence"]

    if similarity >= 0.3 and overlap_ratio >= 0.3:
        return "supported", ["high similarity and token overlap"]

    return "uncertain", ["related evidence found, but stance markers are weak"]
