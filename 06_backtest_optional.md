## 06_backtest_optional.py

This step converts model predictions into a trading simulation.

### Inputs

- `outputs/predictions.csv`:
  - `y_prob_up` (preferred) or `y_pred`
  - `market_ret_1`
  - `close`
- `config.py`:
  - `COST_BPS`, `LONG_ONLY`, `MIN_HOLD_BARS`
- `mode_profile.py`:
  - entry/exit thresholds
  - smoothing/confirmation params
  - hold profile

### Signal mapping (current logic)

When probabilities are available, we:

1. Smooth `y_prob_up` with EWM.
2. Apply hysteresis-style logic:
   - long entry/exit thresholds
   - short entry/exit thresholds
3. Use confirmation bars.
4. Optionally allow direct long↔short flips (mode-dependent).
5. Apply `LONG_ONLY` clipping if needed.

Then we apply minimum holding logic and shift by one bar before trading:

- `position_t = signal_{t-1}`

### Return model

- `strategy_ret = position * market_ret_1 - trading_cost`
- `buyhold_ret = market_ret_1`
- `turnover = abs(position_t - position_{t-1}) / 2`
- `trading_cost = turnover * COST_BPS / 10000`

### Outputs

- `outputs/backtest_metrics.json`
- `outputs/equity_curve.csv`
- `outputs/equity_curve.png`