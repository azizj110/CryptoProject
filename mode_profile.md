## mode_profile.py

This file controls strategy behavior.

We use one pipeline with two personalities:
- conservative
- volatility-sensitive

It reads base settings from `config.py` and returns a parameter dictionary via `get_mode_params()`.

Other scripts consume this dictionary:
- `01_feature_engineering.py` (feature windows, `vol_spike`)
- `03_model_development.py` (volatility sample weighting)
- `06_backtest_optional.py` (thresholds, holding logic, neutral handling)

## Mode logic

We branch on `SAFE_MODE`.

### 1) `SAFE_MODE = True` (conservative)

We reduce noise-chasing and trade less aggressively.

- longer windows:
  - `ret_window=6`
  - `vol_window=12`
  - `sma_fast/sma_slow = 8/24`
  - `autocorr_window=24`
- stricter thresholds:
  - `up_th = max(UP_PROBA_TH, 0.60)`
  - `down_th = min(DOWN_PROBA_TH, 0.40)`
- longer minimum hold:
  - `min_hold = max(MIN_HOLD_BARS, 6)`
- no extra volatility pressure:
  - `enable_vol_spike=False`
  - `vol_weight_gamma=0.0`
- neutral stays neutral:
  - `neutral_to_long=False`

### 2) `SAFE_MODE = False` (aggressive / volatility-sensitive)

We react faster to market variation.

- shorter windows:
  - `ret_window=3`
  - `vol_window=8`
  - `sma_fast/sma_slow = 6/18`
  - `autocorr_window=12`
- more permissive thresholds:
  - `up_th = min(0.55, UP_PROBA_TH - 0.05)`
  - `down_th = max(0.45, DOWN_PROBA_TH + 0.05)`
- shorter hold:
  - `min_hold = min(3, max(1, floor(MIN_HOLD_BARS / 2)))`
- volatility sensitivity enabled:
  - `enable_vol_spike=True`
  - `vol_weight_gamma=0.6`
- neutral can map to long:
  - `neutral_to_long=True`

## Why this file matters

We keep policy decisions separate from implementation details.
That makes experiments cleaner: we can flip one switch and compare behavior under the same data and model setup.