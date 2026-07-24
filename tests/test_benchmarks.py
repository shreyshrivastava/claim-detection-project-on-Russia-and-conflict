from pathlib import Path

from benchmarks.run_benchmarks import run_benchmarks, write_reports


def test_benchmark_smoke_generates_metrics(tmp_path: Path) -> None:
    results = run_benchmarks(iterations=3, smoke=True)
    assert results["benchmarks"]["full_analysis"]["iterations"] == 3
    assert results["benchmarks"]["full_analysis"]["median_ms"] >= 0

    write_reports(results, tmp_path)
    assert (tmp_path / "results.json").exists()
    assert "Benchmark Results" in (tmp_path / "results.md").read_text()
