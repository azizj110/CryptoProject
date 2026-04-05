## 03_model_development.py

This step trains the classifier and generates test-period predictions.

### Inputs

- `processed/features.csv`
- `processed/labels.csv`
- settings from `config.py` and `mode_profile.py`

### Core workflow

1. Merge features + labels on timestamp.
2. Clean NaN/inf and keep only binary labels `{-1, +1}`.
3. Split by fixed date ranges from config (`TRAIN_*`, `TEST_*`).
4. Tune Random Forest with `RandomizedSearchCV` + `TimeSeriesSplit` (macro F1).
5. Train/predict with one of:
   - `one_time`
   - `expanding`
   - `rolling`
6. Save predictions and metadata.

### Model details

- `RandomForestClassifier`
- `class_weight="balanced_subsample"`
- Optional volatility-aware sample weighting from `vol_12` when `vol_weight_gamma > 0`.

### Outputs

- `outputs/predictions.csv` (`y_true`, `y_pred`, `y_prob_up`, `market_ret_1`, `close`)
- `outputs/model_meta.json`
- `artifacts/rf_model.pkl`
- `artifacts/X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`