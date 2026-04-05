## 04_feature_importance.py

This script explains which features matter most to the model.

## Methods we use

1) **MDI**
- Impurity-based importance from the trained Random Forest.

2) **PFI**
- Permutation importance using macro F1.
- For each feature:
  - shuffle the column
  - recompute score
  - measure score drop:
    - `importance = score(original) - score(shuffled)`

## Cluster-level view

We also group features into families:
- momentum
- trend
- volatility
- serial_corr
- regime

Cluster importance is the sum of feature importances inside each family.

## Outputs

- feature-level CSV (MDI + PFI)
- cluster-level CSV (MDI + PFI)
- bar charts for top features and top clusters