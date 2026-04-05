## 04_feature_importance.py

This step explains what the trained model is using.

### Methods

1. **MDI (impurity importance)** from the fitted Random Forest.
2. **PFI (permutation importance)** on test data with `f1_macro`.

### Cluster view

We aggregate feature importances into families:

- momentum
- trend
- volatility
- serial_corr
- regime

### Outputs

- `outputs/mdi_feature_importance.csv`
- `outputs/pfi_feature_importance.csv`
- `outputs/mdi_cluster_importance.csv`
- `outputs/pfi_cluster_importance.csv`
- `outputs/mdi_top_features.png`
- `outputs/pfi_top_features.png`
- `outputs/mdi_cluster_importance.png`
- `outputs/pfi_cluster_importance.png`