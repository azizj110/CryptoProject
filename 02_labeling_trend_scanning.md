## 02_labeling_trend_scanning.py

This script creates targets using trend scanning.

Instead of using one fixed forward horizon, we test several horizons and keep the one with the strongest trend signal.

**Output**
- `processed/labels.csv`

## Inputs

- `prices.csv` (close prices)
- config parameters:
  - `MIN_TREND_H`
  - `MAX_TREND_H`
  - `TREND_STEP`
  - `T_VALUE_MIN`

## Outputs

A time-indexed table with:
- `label` in `{+1, -1, 0}`
- `t_value` (best trend t-stat)
- `horizon` (selected horizon)
- `future_ret` (realized return over selected horizon)

## How it works

1) **Compute slope t-value on each window**
- We use log prices.
- We fit a simple linear trend vs. time.
- We compute the slope t-value.
- If the sample is too short or unstable, we return `0`.

2) **Scan candidate horizons**
- At each timestamp `i`, we test horizons from `min_h` to `max_h` with step `TREND_STEP`.
- We compute t-values on `log(close[i : i+h])`.
- We keep the horizon with the largest absolute t-value.

3) **Assign labels**
- best t-value >= 0 -> `+1`
- best t-value < 0 -> `-1`
- if `abs(best_t_value) < T_VALUE_MIN` -> `0` (weak trend)

4) **Store realized forward return**
- `future_ret = close[i + best_h] / close[i] - 1`
- This is diagnostic output, not a model feature.

## Why we do this

- Log prices improve numerical stability.
- Variable horizons adapt to fast and slow market phases.
- Future data is used only for target creation, not for feature engineering.

## Pipeline role

This is step 2.

`labels.csv` is merged with engineered features in step 3.