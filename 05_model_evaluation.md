## 05_model_evaluation.py

This file is the classification evaluation step  
we take the model predictions on the 2021 test set and compute the core metrics for binary direction signals \(-1,+1\)

### what goes in

- `outputs/predictions.csv`
  - `y_true`
  - `y_pred`

### what comes out

- `outputs/evaluation_metrics.json`
- `outputs/classification_report.txt`
- `outputs/confusion_matrix.csv`
- `outputs/confusion_matrix.png`

---

### evaluation logic

we read predictions then fix class order as `[-1, +1]`  
that matters because confusion matrix rows and columns stay consistent across runs

\[
CM =
\begin{bmatrix}
CM_{-1,-1} & CM_{-1,+1} \\
CM_{+1,-1} & CM_{+1,+1}
\end{bmatrix}
\]

where rows are true labels and columns are predicted labels

---

### metrics computed

- accuracy

\[
\text{Accuracy}=\frac{\#\text{correct}}{N}
\]

- macro precision

\[
\text{Precision}_{macro}=\frac{\text{Precision}_{-1}+\text{Precision}_{+1}}{2}
\]

- macro recall

\[
\text{Recall}_{macro}=\frac{\text{Recall}_{-1}+\text{Recall}_{+1}}{2}
\]

- macro F1

\[
F1_{macro}=\frac{F1_{-1}+F1_{+1}}{2}
\]

we use macro averaging so both classes get equal weight even if class counts differ

---

### why this step matters

this gives the clean model quality view before trading assumptions  
then section 6 backtest converts these predictions into positions and PnL  
so section 5 answers did we classify direction better than chance  
section 6 answers did that become useful strategy returns