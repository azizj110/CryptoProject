## 05_model_evaluation.py

This script evaluates classification quality on the 2021 test set.

Labels are binary direction classes: `-1` and `+1`.

## Input

- `outputs/predictions.csv`:
  - `y_true`
  - `y_pred`

## Outputs

- `outputs/evaluation_metrics.json`
- `outputs/classification_report.txt`
- `outputs/confusion_matrix.csv`
- `outputs/confusion_matrix.png`

## Evaluation flow

- Read predictions.
- Enforce class order `[-1, +1]` for consistent reporting.
- Build confusion matrix:
  - rows = true labels
  - columns = predicted labels

## Reported metrics

- Accuracy
- Macro precision
- Macro recall
- Macro F1

Macro averaging gives both classes equal weight, even if class counts differ.

## Why this matters

This step tells us whether direction classification works.
Backtesting then tells us whether that signal translates into usable trading performance.