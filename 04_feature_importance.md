## 04_feature_importance.py

This file explains which features drive model decisions.

## Methods

1) MDI
- Tree impurity-based importance from the trained Random Forest.

2) PFI
- Permutation importance using macro F1 scoring.
- For each feature:
  - Shuffle one feature column.
  - Recompute score.
  - Importance is score drop:
    - `importance = score(original) - score(shuffled)`

## Cluster view

Features are grouped into families, then importance is summed inside each family.

Families:
- momentum
- trend
- volatility
- serial_corr
- regime

Cluster importance:
- Sum of feature importances within each cluster.

## Outputs

- Feature-level CSV with MDI and PFI
- Cluster-level CSV with MDI and PFI
- Bar charts for top features and top clusters