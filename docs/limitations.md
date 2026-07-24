# Limitations

- This is an evidence-screening demo, not a professional fact-checking system.
- The deployed app is deterministic and lexical; it does not run the historical BERT/SVM model.
- The original datasets and trained model artifacts are not present in the clean repository, so notebook metrics are not independently reproducible.
- Synthetic evaluation results are useful for regression testing, but they are not real-world model quality evidence.
- TF-IDF similarity can miss paraphrases, sarcasm, multilingual text, and semantic entailment.
- Lexical stance markers can misclassify nuanced or multi-sentence evidence.
- Live RSS feeds change over time and can produce non-reproducible behavior.
- Conflict-news analysis can be sensitive; outputs must not be presented as verified truth.

## Before Claiming Model Quality

The project needs:

- original train/validation/test datasets or a documented public dataset
- trained artifacts with checksums or reproducible training scripts
- duplicate and leakage checks across splits
- train/validation/test metric comparison
- error analysis by class and source
- calibration and threshold documentation
- external held-out evaluation, ideally from a different time period or source set
