## 05_model_evaluation.py

This file evaluates classification quality on the 2021 test set.

Labels are binary direction classes: `-1` and `+1`.

## Inputs

- `outputs/predictions.csv`
  - `y_true`
  - `y_pred`

## Outputs

- `outputs/evaluation_metrics.json`
- `outputs/classification_report.txt`
- `outputs/confusion_matrix.csv`
- `outputs/confusion_matrix.png`

## Evaluation logic

- Read predictions.
- Force class order as `[-1, +1]` for stable output layout.
- Build confusion matrix with:
  - Rows = true labels
  - Columns = predicted labels

## Metrics

- Accuracy
- Macro precision
- Macro recall
- Macro F1

Macro averaging gives equal weight to both classes, even if class counts differ.

## Why this step matters

- This step answers: did the model classify direction well?
- Backtest step answers: did this become usable trading performance?