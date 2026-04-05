## mode_profile.py

This file defines the profile-specific behavior used by multiple steps.

`get_mode_params()` returns one dictionary consumed in:

- `01_feature_engineering.py`
- `03_model_development.py`
- `06_backtest_optional.py`

---

## SAFE profile (`SAFE_MODE=True`)

Current parameters:

- `profile="conservative"`
- `ret_window=8`, `vol_window=16`
- `sma_fast=10`, `sma_slow=30`
- `autocorr_window=24`
- `entry_long=0.54`, `exit_long=0.50`
- `entry_short=0.46`, `exit_short=0.50`
- `prob_ewm_span=10`
- `confirm_bars=1`
- `allow_direct_flip=False`
- `min_hold=3`
- `enable_vol_spike=False`
- `vol_weight_gamma=0.0`
- `neutral_to_long=False`

---

## Aggressive profile (`SAFE_MODE=False`)

Current parameters:

- `profile="aggressive"`
- `ret_window=4`, `vol_window=10`
- `sma_fast=6`, `sma_slow=18`
- `autocorr_window=12`
- `entry_long = min(0.56, max(0.51, UP_PROBA_TH - 0.04))`
- `entry_short = max(0.44, min(0.49, DOWN_PROBA_TH + 0.04))`
- `exit_long=0.50`, `exit_short=0.50`
- `up_th/down_th` mirror entry thresholds
- `prob_ewm_span=8`
- `confirm_bars=1`
- `allow_direct_flip=True`
- `min_hold=max(2, MIN_HOLD_BARS // 2)`
- `enable_vol_spike=True`
- `vol_weight_gamma=0.6`
- `neutral_to_long=False`

In short, we use SAFE for slower, stricter behavior and Aggressive for faster, more reactive behavior.