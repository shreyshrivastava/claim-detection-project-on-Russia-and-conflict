"""Model service with an honest deterministic fallback."""

from __future__ import annotations

from dataclasses import dataclass

from claim_detection.config import ArtifactStatus, artifact_status
from claim_detection.evidence import rank_evidence
from claim_detection.pipeline import analyze_claim
from claim_detection.schemas import ClaimAnalysis, EvidenceDocument


@dataclass(frozen=True)
class ModelServiceStatus:
    mode: str
    artifact_available: bool
    missing_artifacts: list[str]
    message: str


class ClaimModelService:
    """Serve claim analysis without pretending missing notebook artifacts exist."""

    def __init__(self, artifacts: ArtifactStatus | None = None) -> None:
        self.artifacts = artifacts or artifact_status()

    @property
    def status(self) -> ModelServiceStatus:
        if self.artifacts.available:
            return ModelServiceStatus(
                mode="artifact_detected_not_loaded",
                artifact_available=True,
                missing_artifacts=[],
                message=(
                    "Historical artifacts are present, but the public app keeps deterministic "
                    "demo mode by default to avoid GPU/model-download assumptions."
                ),
            )
        return ModelServiceStatus(
            mode="deterministic_demo",
            artifact_available=False,
            missing_artifacts=self.artifacts.missing,
            message=(
                "Historical BERT/SVM artifacts are not available; using deterministic "
                "claim screening, evidence ranking, and stance heuristics."
            ),
        )

    def analyze(
        self,
        claim: str,
        documents: list[EvidenceDocument],
        *,
        top_k: int = 3,
    ) -> ClaimAnalysis:
        return analyze_claim(claim, documents, top_k=top_k)

    def rank(
        self,
        claim: str,
        documents: list[EvidenceDocument],
        *,
        top_k: int = 3,
    ):
        return rank_evidence(claim, documents, top_k=top_k)
