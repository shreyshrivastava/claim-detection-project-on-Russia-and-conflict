"""Run deterministic evaluation for the claim evidence checker.

This evaluates the CI-safe deterministic package, not the historical BERT/SVM
notebook model. The fixtures are synthetic and intentionally small, so results
must not be described as real-world model accuracy.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from claim_detection.data import load_default_evidence
from claim_detection.pipeline import analyze_claim

DEFAULT_DATASET = ROOT / "evaluation" / "datasets" / "synthetic_claims.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "evaluation"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on {path}:{line_number}") from exc
    return records


def _accuracy(matches: list[bool]) -> float:
    if not matches:
        return 0.0
    return round(sum(matches) / len(matches), 4)


def run_evaluation(dataset_path: Path = DEFAULT_DATASET, *, smoke: bool = False) -> dict[str, Any]:
    cases = _read_jsonl(dataset_path)
    if smoke:
        cases = cases[:3]

    documents = load_default_evidence()
    rows: list[dict[str, Any]] = []
    deterministic_checks: list[bool] = []

    for case in cases:
        first = analyze_claim(case["claim"], documents)
        second = analyze_claim(case["claim"], documents)
        first_payload = first.to_dict()
        deterministic_checks.append(first_payload == second.to_dict())
        top_evidence_id = first.evidence[0].document.id if first.evidence else None
        rows.append(
            {
                "id": case["id"],
                "claim": case["claim"],
                "expected_verdict": case["expected_verdict"],
                "predicted_verdict": first.verdict,
                "verdict_match": first.verdict == case["expected_verdict"],
                "expected_top_evidence_id": case["expected_top_evidence_id"],
                "predicted_top_evidence_id": top_evidence_id,
                "top_evidence_match": top_evidence_id == case["expected_top_evidence_id"],
                "claim_score": first.signal.claim_score,
                "confidence": first.confidence,
            }
        )

    verdict_matches = [bool(row["verdict_match"]) for row in rows]
    evidence_matches = [bool(row["top_evidence_match"]) for row in rows]
    verdict_counts = Counter(str(row["predicted_verdict"]) for row in rows)

    metrics = {
        "case_count": len(rows),
        "verdict_accuracy": _accuracy(verdict_matches),
        "top_evidence_match_rate": _accuracy(evidence_matches),
        "deterministic_reproducibility": all(deterministic_checks),
        "predicted_verdict_counts": dict(sorted(verdict_counts.items())),
    }

    warnings: list[str] = []
    if len(rows) < 50:
        warnings.append(
            "Small synthetic fixture; do not present these numbers as real-world model accuracy."
        )
    if metrics["top_evidence_match_rate"] >= 0.99:
        warnings.append(
            "Top-evidence ranking uses handcrafted lexical fixtures; 1.0 here is a smoke-test signal."
        )
    if metrics["verdict_accuracy"] >= 0.99:
        warnings.append(
            "Perfect verdict accuracy would be suspicious for model quality; validate on held-out data."
        )

    return {
        "metadata": {
            "generated_at": datetime.now(UTC).isoformat(),
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "dataset": str(dataset_path.relative_to(ROOT)),
            "mode": "smoke" if smoke else "full",
            "evaluated_system": "deterministic claim screening and evidence ranking package",
            "not_evaluated": "historical BERT/SVM notebook model; artifacts are not present",
        },
        "metrics": metrics,
        "warnings": warnings,
        "cases": rows,
    }


def write_reports(results: dict[str, Any], output_dir: Path = DEFAULT_OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "results.json").write_text(json.dumps(results, indent=2) + "\n")

    lines = [
        "# Evaluation Results",
        "",
        "These results evaluate the deterministic package added for reproducible portfolio review. "
        "They do not evaluate the historical BERT/SVM notebook model because the trained artifacts "
        "and original datasets are not present in the clean repository.",
        "",
        "## Metrics",
        "",
        f"- Cases: {results['metrics']['case_count']}",
        f"- Verdict accuracy: {results['metrics']['verdict_accuracy']:.4f}",
        f"- Top-evidence match rate: {results['metrics']['top_evidence_match_rate']:.4f}",
        f"- Deterministic reproducibility: {results['metrics']['deterministic_reproducibility']}",
        "",
        "## Warnings",
        "",
    ]
    lines.extend(f"- {warning}" for warning in results["warnings"])
    lines.extend(["", "## Case Results", ""])
    lines.append(
        "| Case | Expected Verdict | Predicted Verdict | Verdict Match | Expected Evidence | Predicted Evidence |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|")
    for row in results["cases"]:
        lines.append(
            "| {id} | {expected_verdict} | {predicted_verdict} | {verdict_match} | "
            "{expected_top_evidence_id} | {predicted_top_evidence_id} |".format(**row)
        )
    lines.append("")
    (output_dir / "results.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    results = run_evaluation(args.dataset, smoke=args.smoke)
    write_reports(results, args.output_dir)
    print(json.dumps(results["metrics"], indent=2))


if __name__ == "__main__":
    main()
