# Portfolio Project Audit

## Executive Summary

The project started as a notebook-only BERT/SVM claim-detection experiment. That made it weak for a resume because a clean clone could not run the claimed model or reproduce the metrics. The upgrade adds a deployable FastAPI deterministic evidence-screening service, tests, CI, evaluation, benchmarks, Docker/Render configuration, and documentation that clearly separates software reliability from unverified model quality.

## Resume Decision

Supporting resume project.

It is not a flagship project yet because the real BERT/SVM model and datasets are missing. It can support Applied AI Engineer, ML Engineer, and Python Backend Engineer positioning if described honestly as a notebook-to-production hardening project.

## Best Target Roles

- Applied AI Engineer
- Machine Learning Engineer
- LLM/Generative AI Engineer
- Python Backend Engineer
- AI Data Engineer

## Hiring-Manager Scores

| Category | Score |
|---|---:|
| Technical depth | 5 |
| Software engineering quality | 7 |
| AI/ML relevance | 6 |
| Product usefulness | 5 |
| Reliability | 7 |
| Documentation | 8 |
| Deployment readiness | 7 |
| Testing quality | 7 |
| Originality | 4 |
| Resume value | 6 |

Initial overall score: 3.0/10.

Current overall score: 6.2/10.

## Strongest Evidence

- Clean FastAPI package replacing notebook-only execution.
- Deterministic evidence-ranking and stance-screening pipeline.
- 27 local tests covering core logic, API validation, artifact fallback, RSS mocking, evaluation, and benchmarks.
- Synthetic evaluation with non-perfect verdict accuracy, so results are not overclaimed.
- Leakage audit helper for future real model prediction files.
- Docker and Render deployment configuration.

## Weaknesses

- Original BERT/SVM model artifacts are missing.
- Original datasets are missing, so historical notebook metrics are not reproducible.
- No public deployed URL verified yet for this repository.
- Deterministic stance logic is lexical and limited.
- Evidence fixtures are synthetic and small.

## Changes Implemented

- Added `claim_detection/` package with API, CLI, preprocessing, claim scoring, evidence ranking, stance screening, RSS ingestion, and pipeline assembly.
- Added synthetic evidence and evaluation fixtures.
- Added reproducible evaluation and benchmark scripts.
- Added overfitting/leakage audit script.
- Added pytest suite.
- Added GitHub Actions CI and benchmark workflow.
- Added Dockerfile, Render blueprint, runtime file, dependency files, `.gitignore`, and MIT license.
- Rewrote README as a technical case study.
- Added architecture, deployment, limitations, privacy, and notebook audit docs.

## Tests

Latest local result: `27 passed`.

Commands run:

```bash
ruff check .
ruff format --check .
python -m compileall claim_detection evaluation benchmarks tests
pytest
```

## Evaluation

Latest local deterministic evaluation:

- cases: `8`
- verdict accuracy: `0.7500`
- top-evidence match rate: `1.0000`
- deterministic reproducibility: `True`

The top-evidence result is labelled as a handcrafted fixture smoke-test signal, not model accuracy.

## Benchmarks

Latest local deterministic benchmark. These are latency measurements, not accuracy metrics:

- claim scoring median latency: `0.0419 ms`
- evidence ranking median latency: `2.4488 ms`
- full analysis median latency: `2.4862 ms`
- claim scoring median: `0.0456 ms`
- evidence ranking median: `2.2767 ms`
- full analysis median: `2.2747 ms`

Benchmarks exclude BERT embedding generation, live RSS fetching, and deployed network latency.

## Deployment

Prepared for Render using Docker and `render.yaml`.

## Live URL

Not verified yet for this repository.

## CI/CD

CI workflow added for linting, formatting, compilation, tests, deterministic evaluation, benchmark smoke tests, and health-check validation. Benchmark workflow added for manual/path-based full benchmark runs.

## Security and Privacy

No API keys or credentials were added. The deterministic app does not call paid APIs, does not store user claims, and does not intentionally log request bodies. Optional RSS ingestion is network-based but mocked in CI.

## Resume Description

Converted a notebook-only BERT/SVM claim-detection experiment into a deployable FastAPI evidence-screening service with deterministic evaluation, latency benchmarks, CI, Docker, and overfitting audit guardrails.

## Resume Bullets

- Productionized a notebook-based claim-detection experiment into a FastAPI service with deterministic claim scoring, TF-IDF evidence ranking, and coarse stance classification.
- Added 27 pytest tests, GitHub Actions CI, Docker/Render deployment configuration, and API health checks that run without GPUs, model downloads, paid APIs, or live RSS feeds.
- Built synthetic evaluation and latency benchmark pipelines; measured 0.7500 verdict accuracy on 8 synthetic cases and 2.2747 ms median deterministic full-analysis latency locally.
- Added overfitting and leakage audit tooling to flag perfect scores, duplicate split examples, and train-validation/test metric gaps before model metrics are used.

## Remaining Limitations

- Reproduce the original BERT/SVM model from documented datasets.
- Add split leakage checks for real train/validation/test data.
- Deploy and verify a public Render URL.
- Replace synthetic evidence with a documented evidence source.
- Add semantic retrieval or entailment model evaluation if the project is meant to be more than a deterministic demo.

## Recommended Next Step

Deploy the FastAPI service to Render from this branch, then add real model artifacts or a reproducible public dataset only if the leakage audit does not flag overfitting or contamination.
