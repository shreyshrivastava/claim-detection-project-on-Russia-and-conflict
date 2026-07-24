# Benchmark Results

These benchmarks measure deterministic claim screening and evidence ranking only. They do not include BERT embedding generation, live RSS fetching, or a deployed web hop.

## Environment

- Python: 3.14.3
- Platform: macOS-26.5.2-arm64-arm-64bit-Mach-O
- Iterations: 100

## Latency

| Operation | Median ms | P95 ms | Min ms | Max ms | Peak Memory Bytes |
|---|---:|---:|---:|---:|---:|
| claim_scoring | 0.0404 | 0.0492 | 0.0392 | 0.6141 | 26864 |
| evidence_ranking | 1.9732 | 2.0913 | 1.9002 | 4.1859 | 1861802 |
| full_analysis | 1.9996 | 2.1011 | 1.9305 | 2.1560 | 1798338 |
