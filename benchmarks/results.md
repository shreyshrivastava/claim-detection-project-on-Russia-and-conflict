# Benchmark Results

These benchmarks measure deterministic claim screening and evidence ranking only. They do not include BERT embedding generation, live RSS fetching, or a deployed web hop.

## Environment

- Python: 3.14.5
- Platform: macOS-26.5.2-arm64-arm-64bit-Mach-O
- Iterations: 50

## Latency

| Operation | Median ms | P95 ms | Min ms | Max ms | Peak Memory Bytes |
|---|---:|---:|---:|---:|---:|
| claim_scoring | 0.0436 | 0.0492 | 0.0434 | 0.6064 | 26864 |
| evidence_ranking | 2.1576 | 2.3275 | 2.0740 | 5.2882 | 898838 |
| full_analysis | 2.2146 | 2.3142 | 2.1354 | 2.3773 | 915854 |
