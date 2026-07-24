"""Application configuration and artifact discovery."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT_DIR = ROOT_DIR / "artifacts"
DEFAULT_EVIDENCE_PATH = ROOT_DIR / "examples" / "evidence.jsonl"


@dataclass(frozen=True)
class ArtifactStatus:
    """Status for the historical BERT/SVM artifacts expected by the notebooks."""

    artifact_dir: Path
    svm_model: Path
    tokenizer_dir: Path
    bert_weights: Path

    @property
    def available(self) -> bool:
        return (
            self.svm_model.exists() and self.tokenizer_dir.exists() and self.bert_weights.exists()
        )

    @property
    def missing(self) -> list[str]:
        missing: list[str] = []
        if not self.svm_model.exists():
            missing.append(str(self.svm_model))
        if not self.tokenizer_dir.exists():
            missing.append(str(self.tokenizer_dir))
        if not self.bert_weights.exists():
            missing.append(str(self.bert_weights))
        return missing


def artifact_status(artifact_dir: str | Path | None = None) -> ArtifactStatus:
    """Return expected model artifact paths without downloading anything."""

    root = Path(artifact_dir or os.getenv("CLAIM_DETECTION_ARTIFACT_DIR") or DEFAULT_ARTIFACT_DIR)
    return ArtifactStatus(
        artifact_dir=root,
        svm_model=root / "svm_model.joblib",
        tokenizer_dir=root / "bert-base-uncased-tokenizer",
        bert_weights=root / "bert_model.pth",
    )
