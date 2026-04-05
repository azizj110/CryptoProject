## 02_labeling_trend_scanning.py

This file creates model targets using trend scanning.

Instead of a fixed forward horizon, it tests multiple horizons and keeps the one with the strongest trend signal.

Output file:
- `processed/labels.csv`

## Inputs

- `prices.csv` (close series)
- Config values:
  - `MIN_TREND_H`
  - `MAX_TREND_H`
  - `TREND_STEP`
  - `T_VALUE_MIN`

## Outputs

Time-indexed label table with:
- `label` in `{+1, -1, 0}`
- `t_value` (best trend t-stat)
- `horizon` (selected forward horizon)
- `future_ret` (realized return over selected horizon)

## Core logic

1) Slope t-value on a window
- Use log prices on the candidate window.
- Fit a simple linear trend against time index.
- Compute slope t-value.
- If sample is too short or numerically unstable, return `0`.

2) Trend scan at each timestamp
- For each start index `i`, test horizons from `min_h` to `max_h` with step `TREND_STEP`.
- Compute t-value on `log(close[i : i+h])`.
- Pick the horizon with largest absolute t-value.

3) Label assignment
- If best t-value is positive or zero, label is `+1`.
- If best t-value is negative, label is `-1`.
- If `abs(best_t_value) < T_VALUE_MIN`, label is `0` (weak trend).

4) Realized forward return
- `future_ret = close[i + best_h] / close[i] - 1`
- This is for diagnostics and analysis, not a model feature.

## Design notes

- Log prices are used for better stability.
- Variable horizons let labels adapt to local market speed.
- First and last rows may be unlabeled when forward data is missing.
- This step uses future data only for target creation, not for feature generation.

## Pipeline role

This is step 2 of the project.

`labels.csv` is merged with engineered features in step 3 for model training.