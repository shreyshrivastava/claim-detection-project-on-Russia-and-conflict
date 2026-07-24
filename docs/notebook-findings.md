# Notebook Findings

The original repository contained two notebooks:

- `BERT and SVM Final model for claim-detection and fact-checking .ipynb`
- `Ukraine,_Russia_conflict_testing_on_RSS_feed.ipynb`

## Verified From Notebook Output

The training notebook records:

- 5-fold validation accuracy: `0.8817 (+/- 0.0058)`
- 5-fold validation F1: `0.8810 (+/- 0.0059)`
- test accuracy: `0.9061`
- test F1: `0.9068`
- test recall: `0.9061`
- test precision: `0.9078`

These are notebook output logs, not metrics reproduced from the clean repository.

## Missing From Clean Repository

The notebooks reference artifacts that are not tracked:

- `ru22fact_train.csv`
- `ru22fact_validate.csv`
- `ru22fact_test.csv`
- trained BERT weights
- trained SVM/joblib artifacts

Because these files are missing, a fresh clone cannot reproduce the historical model, training run, or RSS inference notebook.

## Overfitting and Leakage Risks

The visible notebook code does not show a perfect score, but the current repository still needs stronger validation before model performance can be used on a resume:

- Split duplicate checks are not shown.
- `KFold` is used instead of `StratifiedKFold`, which may be less stable if labels are imbalanced.
- Claims and evidence are concatenated, so near-duplicate claim/evidence pairs across splits could inflate metrics.
- The RSS notebook uses live feeds, which are not reproducible and can change without code changes.
- Model artifacts are not checksummed or versioned.

## Added Guardrail

`evaluation/generalization_audit.py` can audit real train/validation/test prediction CSV files. It flags:

- suspicious perfect scores
- small split sizes
- duplicate text keys across splits
- train-validation accuracy gaps over 10 percentage points
- validation-test accuracy gaps over 10 percentage points
