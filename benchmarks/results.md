# Benchmark Results

These benchmarks measure deterministic claim screening and evidence ranking only. They do not include BERT embedding generation, live RSS fetching, or a deployed web hop.

## Environment

- Python: 3.12.13
- Platform: macOS-26.5.2-arm64-arm-64bit
- Iterations: 50

## Latency

| Operation | Median ms | P95 ms | Min ms | Max ms | Peak Memory Bytes |
|---|---:|---:|---:|---:|---:|
| claim_scoring | 0.0419 | 0.0425 | 0.0394 | 1.3095 | 27488 |
| evidence_ranking | 2.4488 | 2.5352 | 2.3197 | 5.8024 | 759481 |
| full_analysis | 2.4862 | 2.5455 | 2.3738 | 2.8485 | 601017 |
