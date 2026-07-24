"""Run lightweight latency benchmarks for deterministic claim analysis."""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import time
import tracemalloc
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from claim_detection.claim_detector import score_claim
from claim_detection.data import load_default_evidence
from claim_detection.evidence import rank_evidence
from claim_detection.pipeline import analyze_claim

DEFAULT_OUTPUT_DIR = ROOT / "benchmarks"


def _summary(values: list[float]) -> dict[str, float | int]:
    if not values:
        return {"iterations": 0, "median_ms": 0.0, "p95_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}
    ordered = sorted(values)
    p95_index = min(len(ordered) - 1, int(round((len(ordered) - 1) * 0.95)))
    return {
        "iterations": len(values),
        "median_ms": round(statistics.median(values), 4),
        "p95_ms": round(ordered[p95_index], 4),
        "min_ms": round(ordered[0], 4),
        "max_ms": round(ordered[-1], 4),
    }


def _measure(
    operation: Callable[[], object], iterations: int
) -> tuple[dict[str, float | int], int]:
    values: list[float] = []
    tracemalloc.start()
    for _ in range(iterations):
        started = time.perf_counter()
        operation()
        values.append((time.perf_counter() - started) * 1000)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return _summary(values), peak


def run_benchmarks(*, iterations: int = 50, smoke: bool = False) -> dict[str, object]:
    if smoke:
        iterations = min(iterations, 5)

    documents = load_default_evidence()
    claim = (
        "The International Relief Mission delivered 20 generators to Northport hospital on Tuesday."
    )

    claim_scoring, claim_peak = _measure(lambda: score_claim(claim), iterations)
    evidence_ranking, evidence_peak = _measure(lambda: rank_evidence(claim, documents), iterations)
    full_analysis, analysis_peak = _measure(lambda: analyze_claim(claim, documents), iterations)

    return {
        "metadata": {
            "generated_at": datetime.now(UTC).isoformat(),
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "iterations": iterations,
            "mode": "smoke" if smoke else "full",
            "methodology": "Local deterministic latency measurements; no BERT, RSS, network, or paid API calls.",
        },
        "benchmarks": {
            "claim_scoring": {**claim_scoring, "peak_memory_bytes": claim_peak},
            "evidence_ranking": {**evidence_ranking, "peak_memory_bytes": evidence_peak},
            "full_analysis": {**full_analysis, "peak_memory_bytes": analysis_peak},
        },
    }


def write_reports(results: dict[str, object], output_dir: Path = DEFAULT_OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "results.json").write_text(json.dumps(results, indent=2) + "\n")

    lines = [
        "# Benchmark Results",
        "",
        "These benchmarks measure deterministic claim screening and evidence ranking only. "
        "They do not include BERT embedding generation, live RSS fetching, or a deployed web hop.",
        "",
        "## Environment",
        "",
        f"- Python: {results['metadata']['python']}",
        f"- Platform: {results['metadata']['platform']}",
        f"- Iterations: {results['metadata']['iterations']}",
        "",
        "## Latency",
        "",
        "| Operation | Median ms | P95 ms | Min ms | Max ms | Peak Memory Bytes |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, metrics in results["benchmarks"].items():
        lines.append(
            f"| {name} | {metrics['median_ms']:.4f} | {metrics['p95_ms']:.4f} | "
            f"{metrics['min_ms']:.4f} | {metrics['max_ms']:.4f} | {metrics['peak_memory_bytes']} |"
        )
    lines.append("")
    (output_dir / "results.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.iterations < 1:
        raise SystemExit("--iterations must be positive")
    results = run_benchmarks(iterations=args.iterations, smoke=args.smoke)
    write_reports(results, args.output_dir)
    print(json.dumps(results["benchmarks"], indent=2))


if __name__ == "__main__":
    main()
