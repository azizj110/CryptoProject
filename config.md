## config.py

This file is the single source of truth for project settings.

We keep all global parameters here so runs stay reproducible and easy to audit.

## What it controls

### 1) Paths
- `BASE_DIR`
- `RAW_DATA_PATH`
- `PROCESSED_DIR`
- `OUTPUT_DIR`
- `ARTIFACTS_DIR`

This keeps file handling consistent and avoids hardcoded paths.

### 2) Global experiment settings
- `RANDOM_STATE` for reproducibility
- `TEST_SIZE` (legacy split ratio from older versions)

For the current assignment, we use explicit date ranges.

### 3) Trend-scanning label parameters
- `MIN_TREND_H`
- `MAX_TREND_H`
- `TREND_STEP`
- `T_VALUE_MIN`

These values control horizon search and label strictness.

### 4) Training strategy
- `TRAINING_STRATEGY` = `one_time | expanding | rolling`
- `REFIT_EVERY`
- `ROLLING_WINDOW`

For assignment-compliant evaluation, we typically use `one_time`:
train once on 2018–2020, then test on 2021.

### 5) Required date split
- `TRAIN_START`, `TRAIN_END`
- `TEST_START`, `TEST_END`

This enforces exact train/test periods and helps prevent leakage.

### 6) Backtest settings
- `COST_BPS` transaction cost in basis points
- `UP_PROBA_TH`, `DOWN_PROBA_TH` signal thresholds
- `LONG_ONLY` to disable shorting
- `MIN_HOLD_BARS` to reduce churn

These parameters control how probabilities turn into positions.

### 7) Sensitivity mode switch
- `SAFE_MODE`

Meaning in this project:
- `SAFE_MODE=True`: conservative behavior (higher thresholds, longer holds)
- `SAFE_MODE=False`: more volatility-sensitive behavior (faster reactions)

Detailed mode behavior lives in `mode_profile.py`.

## Why this file matters

By centralizing assumptions, we make outputs easier to explain and experiments easier to compare.