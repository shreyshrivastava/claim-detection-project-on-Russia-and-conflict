"""Deterministic claim-likelihood scoring."""

from __future__ import annotations

import re

from claim_detection.preprocessing import normalize_text, tokenize
from claim_detection.schemas import ClaimSignal

ASSERTIVE_VERBS = {
    "announced",
    "approved",
    "confirmed",
    "delivered",
    "deployed",
    "denied",
    "documented",
    "opened",
    "reported",
    "reopened",
    "restarted",
    "said",
    "signed",
    "suspended",
    # Action and conflict verbs
    "launched",
    "attacked",
    "struck",
    "destroyed",
    "seized",
    "captured",
    "killed",
    "injured",
    "targeted",
    "fired",
    "advanced",
    "retreated",
    "withdrew",
    "invaded",
    "counterattack",
    "counterattacks",
    "offensive",
    "defenses",
    "defense",
    # Statement and reporting verbs
    "claimed",
    "stated",
    "asserted",
    "alleged",
    "accused",
    "rejected",
    "condemned",
    "declared",
    "warned",
    "called",
    "demanded",
    "agreed",
    "met",
    "discussed",
    "visited",
    "hosted",
    "pledged",
    "promised",
    "criticized",
    # Occurrence and result verbs
    "occurred",
    "happened",
    "began",
    "ended",
    "ceased",
    "fails",
    "failed",
    "succeeds",
    "succeeded",
}

HEDGING_TERMS = {
    "allegedly",
    "could",
    "may",
    "might",
    "possibly",
    "rumor",
    "reportedly",
    "unconfirmed",
}


def score_claim(text: str) -> ClaimSignal:
    """Score whether a sentence is an atomic factual claim.

    This is a deterministic screening signal, not a truth classifier.
    """

    cleaned = normalize_text(text)
    tokens = tokenize(cleaned, remove_stopwords=False)
    content_tokens = tokenize(cleaned)
    token_set = set(tokens)
    rationale: list[str] = []

    has_number = bool(re.search(r"\b\d+(?:\.\d+)?\b", cleaned))
    has_date = bool(
        re.search(
            r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|"
            r"march|april|may|june|july|august|september|october|november|december|today|"
            r"yesterday|tomorrow|morning|afternoon|evening|midnight|202\d)\b",
            cleaned.lower(),
        )
    )
    assertive_count = len(token_set & ASSERTIVE_VERBS)
    hedging_count = len(token_set & HEDGING_TERMS)
    named_entity_like = len(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", cleaned))

    score = 0.0
    if len(content_tokens) >= 5:
        score += 0.2
        rationale.append("contains enough content words for factual screening")
    if assertive_count:
        score += min(0.35, assertive_count * 0.2)
        rationale.append("uses assertive event/reporting language")
    if has_number:
        score += 0.15
        rationale.append("contains a numeric detail")
    if has_date:
        score += 0.1
        rationale.append("contains a time reference")
    if named_entity_like:
        score += min(0.2, named_entity_like * 0.05)
        rationale.append("contains named-entity-like terms")
    if "?" in cleaned:
        score -= 0.2
        rationale.append("question form reduces claim likelihood")
    if hedging_count:
        score -= min(0.2, hedging_count * 0.1)
        rationale.append("hedging terms reduce claim certainty")

    score = round(max(0.0, min(score, 1.0)), 4)
    return ClaimSignal(
        is_claim=score >= 0.35,
        claim_score=score,
        features={
            "token_count": len(tokens),
            "content_token_count": len(content_tokens),
            "assertive_terms": assertive_count,
            "hedging_terms": hedging_count,
            "has_number": int(has_number),
            "has_date": int(has_date),
            "named_entity_like_terms": named_entity_like,
        },
        rationale=rationale or ["insufficient factual detail detected"],
    )
