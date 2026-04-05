## config.py

This file is our central experiment configuration.

### Paths

- `RAW_DATA_PATH`
- `PROCESSED_DIR`
- `OUTPUT_DIR`
- `ARTIFACTS_DIR`

### Data split and reproducibility

- `RANDOM_STATE`
- Fixed train/test periods (`TRAIN_*`, `TEST_*`)
- `TEST_SIZE` is present but not used in the fixed-date split pipeline.

### Labeling setup

- `MIN_TREND_H`
- `MAX_TREND_H`
- `TREND_STEP`
- `T_VALUE_MIN`

### Training strategy

- `TRAINING_STRATEGY = one_time | expanding | rolling`
- `REFIT_EVERY`
- `ROLLING_WINDOW`

### Backtest controls

- `COST_BPS`
- `UP_PROBA_TH`, `DOWN_PROBA_TH`
- `LONG_ONLY`
- `MIN_HOLD_BARS`

### Mode switch

- `SAFE_MODE` selects profile behavior in `mode_profile.py`.
- In the current code, `SAFE_MODE=True` maps to the conservative profile, and `SAFE_MODE=False` to the aggressive profile.