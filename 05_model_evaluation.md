## 05_model_evaluation.py

This step evaluates classification quality on the test period.

### Input

- `outputs/predictions.csv` (`y_true`, `y_pred`)

### What we compute

Using fixed class order `[-1, +1]`:

- Accuracy
- Precision (macro)
- Recall (macro)
- F1 (macro)
- Confusion matrix
- Full text classification report

### Outputs

- `outputs/evaluation_metrics.json`
- `outputs/classification_report.txt`
- `outputs/confusion_matrix.csv`
- `outputs/confusion_matrix.png`

Macro metrics are used so both classes have equal weight.