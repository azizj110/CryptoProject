## 04_feature_importance.py

This file explains what drives model decisions

### methods

1) MDI (tree impurity importance)  
2) PFI (permutation importance with macro f1 scoring)

for PFI we measure score drop after shuffling one feature

`importance_j = score(X,y) - score(shuffle_j(X), y)`

### cluster view

we group features by families and sum importances inside each cluster

- momentum
- trend
- volatility
- serial_corr
- regime

`cluster_importance = sum(feature_importance in cluster)`

### outputs

- feature-level csv: MDI and PFI
- cluster-level csv: MDI and PFI
- bar charts for top features and clusters