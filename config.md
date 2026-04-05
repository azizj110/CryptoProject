## config.py

This file is the single source of truth for project settings  
we keep all global knobs here so experiments stay reproducible and easy to audit

### what it controls

### 1) paths

- `BASE_DIR`
- `RAW_DATA_PATH`
- `PROCESSED_DIR`
- `OUTPUT_DIR`
- `ARTIFACTS_DIR`

This keeps every script path consistent and avoids hardcoded locations

### 2) global experiment settings

- `RANDOM_STATE` for reproducibility
- `TEST_SIZE` legacy split ratio used in older versions  
  current assignment run uses explicit date ranges instead

### 3) trend scanning label parameters

- `MIN_TREND_H`
- `MAX_TREND_H`
- `TREND_STEP`
- `T_VALUE_MIN`

These govern how section 2 searches forward horizons and how strict labels are  
larger horizon range can capture slower trends while larger `T_VALUE_MIN` filters weak trends

### 4) training strategy controls

- `TRAINING_STRATEGY` = `one_time | expanding | rolling`
- `REFIT_EVERY`
- `ROLLING_WINDOW`

for assignment compliant evaluation we typically use `one_time`  
train on 2018 to 2020 once then test on 2021

### 5) required assignment date split

- `TRAIN_START`, `TRAIN_END`
- `TEST_START`, `TEST_END`

this is the key part that enforces no leakage and exact period logic

### 6) backtest controls

- `COST_BPS` transaction cost in basis points
- `UP_PROBA_TH`, `DOWN_PROBA_TH` probability thresholds for signal generation
- `LONG_ONLY` whether to disable shorting
- `MIN_HOLD_BARS` minimum holding period to reduce churn

These settings determine how predicted probabilities become tradable positions

### 7) sensitivity mode switch

- `SAFE_MODE`

Current meaning in this project design

- `SAFE_MODE=True`  
  conservative behavior less reactive to noise usually higher thresholding and longer holds
- `SAFE_MODE=False`  
  more volatility sensitive behavior faster reaction more variation capture

actual per mode details are defined in `mode_profile.py`

---

### why this file matters

it centralizes all assumptions in one place  
that makes results explainable because every output can be tied to explicit config values  
and it supports fair comparisons between runs by changing one parameter set at a time