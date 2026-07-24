# Evaluation Results

These results evaluate the deterministic package added for reproducible portfolio review. They do not evaluate the historical BERT/SVM notebook model because the trained artifacts and original datasets are not present in the clean repository.

## Metrics

- Cases: 8
- Verdict accuracy: 0.7500
- Top-evidence match rate: 1.0000
- Deterministic reproducibility: True

## Warnings

- Small synthetic fixture; do not present these numbers as real-world model accuracy.
- Top-evidence ranking uses handcrafted lexical fixtures; 1.0 here is a smoke-test signal.

## Case Results

| Case | Expected Verdict | Predicted Verdict | Verdict Match | Expected Evidence | Predicted Evidence |
|---|---:|---:|---:|---:|---:|
| case-001 | supported | supported | True | doc-001 | doc-001 |
| case-002 | refuted | refuted | True | doc-002 | doc-002 |
| case-003 | supported | supported | True | doc-003 | doc-003 |
| case-004 | uncertain | refuted | False | doc-005 | doc-005 |
| case-005 | not_a_clear_claim | not_a_clear_claim | True | doc-004 | doc-004 |
| case-006 | uncertain | not_a_clear_claim | False | doc-006 | doc-006 |
| case-007 | supported | supported | True | doc-007 | doc-007 |
| case-008 | refuted | refuted | True | doc-008 | doc-008 |
