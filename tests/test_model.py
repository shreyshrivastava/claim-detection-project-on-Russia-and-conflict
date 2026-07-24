from pathlib import Path

from claim_detection.config import artifact_status
from claim_detection.data import load_default_evidence
from claim_detection.model import ClaimModelService


def test_artifact_status_reports_missing_artifacts(tmp_path: Path) -> None:
    status = artifact_status(tmp_path)

    assert status.available is False
    assert len(status.missing) == 3


def test_model_service_uses_deterministic_demo_without_artifacts(tmp_path: Path) -> None:
    service = ClaimModelService(artifact_status(tmp_path))
    result = service.analyze(
        "The International Relief Mission delivered 20 generators to Northport hospital on Tuesday.",
        load_default_evidence(),
    )

    assert service.status.mode == "deterministic_demo"
    assert result.verdict == "supported"
