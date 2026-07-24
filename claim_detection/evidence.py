"""Evidence ranking utilities."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from claim_detection.preprocessing import tokenize
from claim_detection.schemas import EvidenceDocument, EvidenceMatch
from claim_detection.stance import classify_stance


def _overlap_ratio(claim: str, evidence: str) -> float:
    claim_tokens = set(tokenize(claim))
    evidence_tokens = set(tokenize(evidence))
    if not claim_tokens:
        return 0.0
    return round(len(claim_tokens & evidence_tokens) / len(claim_tokens), 4)


def rank_evidence(
    claim: str,
    documents: Iterable[EvidenceDocument],
    *,
    top_k: int = 3,
) -> list[EvidenceMatch]:
    """Rank evidence documents by TF-IDF cosine similarity."""

    docs = list(documents)
    if not claim.strip() or not docs:
        return []
    if top_k < 1:
        raise ValueError("top_k must be positive")

    corpus = [claim] + [f"{doc.title}. {doc.text}" for doc in docs]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
    matrix = vectorizer.fit_transform(corpus)
    similarities = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    ranked_indexes = np.argsort(similarities)[::-1][:top_k]

    matches: list[EvidenceMatch] = []
    for index in ranked_indexes:
        doc = docs[int(index)]
        similarity = round(float(similarities[int(index)]), 4)
        overlap = _overlap_ratio(claim, f"{doc.title}. {doc.text}")
        stance, rationale = classify_stance(claim, f"{doc.title}. {doc.text}", similarity, overlap)
        matches.append(
            EvidenceMatch(
                document=doc,
                similarity=similarity,
                overlap_ratio=overlap,
                stance=stance,
                rationale=rationale,
            )
        )
    return matches
