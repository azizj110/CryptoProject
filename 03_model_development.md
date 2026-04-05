## 03_model_development.py

This script trains the classifier and produces out-of-sample predictions.

**Model**
- Random Forest
- binary direction labels: `-1`, `+1`

## Inputs

- `processed/features.csv`
- `processed/labels.csv`
- `config.py`:
  - fixed split:
    - train: `2018-01-01` to `2020-12-31`
    - test: `2021-01-01` to `2021-12-31`
  - `TRAINING_STRATEGY` (`one_time`, `expanding`, `rolling`)
  - seed and refit settings
- `mode_profile.py`:
  - volatility sensitivity settings such as `vol_weight_gamma`

## Workflow

1) **Merge and clean**
- Join features and labels by timestamp.
- Drop NaN/inf rows.
- Keep labels in `{-1, +1}` only.
- Sort chronologically.
- Remove non-feature columns (for example: `label`, `close`, `market_ret_1`, diagnostics).

2) **Split by date**
- Train on 2018–2020.
- Test on 2021.

3) **Tune and train**
- Base model: `RandomForestClassifier` with class balancing.
- Tune with `RandomizedSearchCV` + `TimeSeriesSplit`.
- Optimize macro F1.
- Search parameters:
  - `n_estimators`
  - `max_depth`
  - `min_samples_leaf`
  - `max_features`

4) **Optional volatility-aware weighting**
- Used when `vol_weight_gamma > 0`.
- Based on `vol_12`.
- We compute a robust z-score (median + MAD).
- Weight: `w = 1 + gamma * clip(z, 0, 3)`.

5) **Training mode**
- `one_time`: one fit on 2018–2020, then predict full 2021.
- `expanding` / `rolling`: walk-forward refits.

## Outputs

Predictions:
- `outputs/predictions.csv`:
  - `y_true`
  - `y_pred`
  - `y_prob_up`
  - `market_ret_1`
  - `close`

Artifacts:
- `artifacts/rf_model.pkl`
- `artifacts/X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`

Metadata:
- `outputs/model_meta.json` (periods, counts, best params, CV score)

## Why this design

We use trees for nonlinear behavior, time-aware validation to reduce leakage risk, and saved metadata for reproducibility.