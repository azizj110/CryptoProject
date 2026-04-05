## 03_model_development.py

This file trains the main classifier and generates out-of-sample predictions.

Model:
- Random Forest
- Binary direction labels: `-1` and `+1`

## Inputs

- `processed/features.csv`
- `processed/labels.csv`
- `config.py` settings:
  - Fixed split:
    - Train: `2018-01-01` to `2020-12-31`
    - Test: `2021-01-01` to `2021-12-31`
  - Training strategy (`one_time`, `expanding`, `rolling`)
  - Random seed and refit settings
- `mode_profile.py` settings (for volatility sensitivity), including `vol_weight_gamma`

## Steps

1) Merge and clean
- Join features and labels by timestamp.
- Drop NaN and inf rows.
- Keep only labels in `{-1, +1}`.
- Sort by time.
- Remove non-feature columns from training matrix:
  - `label`, `close`, `market_ret_1`, and diagnostics columns

2) Fixed period split
- Chronological split by date:
  - Train: 2018 to 2020
  - Test: 2021

3) Model and tuning
- Base model: `RandomForestClassifier` with class balancing.
- Tune with `RandomizedSearchCV` and `TimeSeriesSplit`.
- Objective metric: macro F1.
- Tuned params:
  - `n_estimators`
  - `max_depth`
  - `min_samples_leaf`
  - `max_features`

4) Volatility-aware sample weighting (optional)
- Enabled when `vol_weight_gamma > 0`.
- Uses `vol_12` feature.
- Build robust z-score with median and MAD.
- Weight formula:
  - `w = 1 + gamma * clip(z, 0, 3)`
- Effect: high-volatility rows can receive more weight.

5) Training strategy
- `one_time`: train once on 2018-2020, predict all 2021.
- `expanding` or `rolling`: walk-forward refits and next-block prediction.
- For strict assignment compliance, `one_time` is the cleanest setting.

6) Outputs

Predictions:
- `outputs/predictions.csv`
  - `y_true`
  - `y_pred`
  - `y_prob_up` (probability of class `+1`)
  - `market_ret_1`, `close`

Artifacts:
- `artifacts/rf_model.pkl`
- `artifacts/X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`

Metadata:
- `outputs/model_meta.json`
  - periods
  - row counts
  - best parameters
  - CV score

## Why this design

- Tree models handle nonlinear relationships well.
- Time-aware CV respects sequence order.
- Saved metadata improves reproducibility.