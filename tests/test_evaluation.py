from pathlib import Path

from evaluation.generalization_audit import PredictionRecord, audit_splits
from evaluation.run_evaluation import run_evaluation, write_reports


def test_run_evaluation_reports_non_perfect_verdict_accuracy() -> None:
    results = run_evaluation()
    assert results["metrics"]["case_count"] == 8
    assert results["metrics"]["verdict_accuracy"] < 1.0
    assert results["metrics"]["deterministic_reproducibility"] is True
    assert any("Small synthetic fixture" in warning for warning in results["warnings"])


def test_write_evaluation_reports(tmp_path: Path) -> None:
    results = run_evaluation(smoke=True)
    write_reports(results, tmp_path)
    assert (tmp_path / "results.json").exists()
    assert "Evaluation Results" in (tmp_path / "results.md").read_text()


def test_generalization_audit_flags_perfect_train_scores_and_duplicates() -> None:
    results = audit_splits(
        {
            "train": [
                PredictionRecord("supported", "supported", "same-claim"),
                PredictionRecord("refuted", "refuted", "train-only"),
            ],
            "validation": [
                PredictionRecord("supported", "refuted", "same-claim"),
                PredictionRecord("refuted", "refuted", "validation-only"),
            ],
        }
    )

    warnings = " ".join(results["warnings"])
    assert "perfect score" in warnings
    assert "Duplicate text keys" in warnings
