## 02_labeling_trend_scanning.py

This step creates supervised labels with trend scanning and saves:

- `processed/labels.csv`

### Inputs

From `config.py`:

- `MIN_TREND_H`
- `MAX_TREND_H`
- `TREND_STEP`
- `T_VALUE_MIN`

### How we label

For each timestamp, we:

1. Scan multiple forward horizons.
2. Compute slope t-value on log-price windows.
3. Keep the horizon with maximum `abs(t_value)`.
4. Assign:
   - `+1` if best trend is positive
   - `-1` if best trend is negative
   - `0` if `abs(t_value) < T_VALUE_MIN`
5. Store `future_ret` for diagnostics.

### Output columns

- `label`
- `t_value`
- `horizon`
- `future_ret`

Rows near the end may remain empty when no valid horizon exists.