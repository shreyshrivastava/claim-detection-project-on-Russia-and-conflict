# Benchmark Results

These benchmarks measure deterministic claim screening and evidence ranking only. They do not include BERT embedding generation, live RSS fetching, or a deployed web hop.

## Environment

- Python: 3.14.5
- Platform: macOS-26.5.2-arm64-arm-64bit-Mach-O
- Iterations: 50

## Latency

| Operation | Median ms | P95 ms | Min ms | Max ms | Peak Memory Bytes |
|---|---:|---:|---:|---:|---:|
| claim_scoring | 0.0456 | 0.0905 | 0.0441 | 0.6381 | 26864 |
| evidence_ranking | 2.2767 | 2.4855 | 2.1578 | 5.6855 | 906192 |
| full_analysis | 2.2747 | 2.4567 | 2.1791 | 2.5944 | 924923 |
