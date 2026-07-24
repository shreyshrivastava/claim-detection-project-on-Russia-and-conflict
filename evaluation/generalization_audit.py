"""Audit train/validation/test prediction files for overfitting signals."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sklearn.metrics import accuracy_score, precision_recall_fscore_support


@dataclass(frozen=True)
class PredictionRecord:
    label: str
    prediction: str
    text_key: str | None = None


def load_prediction_csv(path: Path) -> list[PredictionRecord]:
    """Load labels/predictions from CSV.

    Required columns: label, prediction.
    Optional columns: text_key or claim_id for duplicate-leakage checks.
    """

    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"label", "prediction"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path} must contain label and prediction columns")
        key_column = "text_key" if "text_key" in reader.fieldnames else "claim_id"
        return [
            PredictionRecord(
                label=row["label"].strip(),
                prediction=row["prediction"].strip(),
                text_key=(row.get(key_column) or "").strip() or None,
            )
            for row in reader
        ]


def _split_metrics(records: list[PredictionRecord]) -> dict[str, float | int]:
    if not records:
        return {"count": 0, "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}

    labels = [record.label for record in records]
    predictions = [record.prediction for record in records]
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="weighted",
        zero_division=0,
    )
    return {
        "count": len(records),
        "accuracy": round(float(accuracy_score(labels, predictions)), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1": round(float(f1), 4),
    }


def audit_splits(splits: dict[str, list[PredictionRecord]]) -> dict[str, Any]:
    """Compute metrics and warnings that help detect overfit or leakage."""

    metrics = {name: _split_metrics(records) for name, records in splits.items()}

    key_to_splits: dict[str, set[str]] = defaultdict(set)
    for split_name, records in splits.items():
        for record in records:
            if record.text_key:
                key_to_splits[record.text_key].add(split_name)

    duplicate_keys = sorted(
        key for key, split_names in key_to_splits.items() if len(split_names) > 1
    )
    warnings: list[str] = []

    for split_name, split_metrics in metrics.items():
        if split_metrics["count"] and split_metrics["count"] < 30:
            warnings.append(f"{split_name} has fewer than 30 examples; metrics are unstable.")
        if split_metrics["accuracy"] >= 0.999 or split_metrics["f1"] >= 0.999:
            warnings.append(
                f"{split_name} reports a perfect score; inspect for leakage, duplicates, or label shortcuts."
            )

    if duplicate_keys:
        warnings.append(
            "Duplicate text keys appear across splits; this can inflate validation/test metrics."
        )

    train = metrics.get("train", {})
    validation = metrics.get("validation", {})
    test = metrics.get("test", {})
    if train and validation and train.get("accuracy", 0) - validation.get("accuracy", 0) > 0.1:
        warnings.append(
            "Train accuracy exceeds validation accuracy by more than 10 percentage points."
        )
    if validation and test and validation.get("accuracy", 0) - test.get("accuracy", 0) > 0.1:
        warnings.append(
            "Validation accuracy exceeds test accuracy by more than 10 percentage points."
        )

    return {
        "metrics": metrics,
        "duplicate_text_keys": duplicate_keys[:100],
        "duplicate_text_key_count": len(duplicate_keys),
        "warnings": warnings,
    }


def write_audit(results: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "generalization-audit.json").write_text(json.dumps(results, indent=2) + "\n")
    lines = [
        "# Generalization Audit",
        "",
        "Use this report when real train/validation/test predictions are available. "
        "It is designed to catch overfitting indicators, suspicious perfect metrics, "
        "and duplicate examples across splits.",
        "",
        "## Metrics",
        "",
    ]
    for split_name, metrics in results["metrics"].items():
        lines.append(
            f"- {split_name}: n={metrics['count']}, accuracy={metrics['accuracy']:.4f}, "
            f"F1={metrics['f1']:.4f}"
        )
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in results["warnings"])
    if not results["warnings"]:
        lines.append("- No overfitting warning thresholds were triggered.")
    lines.append("")
    (output_dir / "generalization-audit.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=Path)
    parser.add_argument("--validation", type=Path)
    parser.add_argument("--test", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("evaluation"))
    args = parser.parse_args()

    provided = {
        "train": args.train,
        "validation": args.validation,
        "test": args.test,
    }
    splits = {name: load_prediction_csv(path) for name, path in provided.items() if path}
    if not splits:
        raise SystemExit("Provide at least one of --train, --validation, or --test.")
    results = audit_splits(splits)
    write_audit(results, args.output_dir)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
