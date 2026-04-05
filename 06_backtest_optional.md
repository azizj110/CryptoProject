## 06_backtest_optional.py

This file converts model predictions into a trading simulation on the test period.

It is optional in pipeline order, but useful to check whether prediction quality turns into PnL.

## Inputs

- `outputs/predictions.csv`
  - `y_pred`
  - optional `y_prob_up`
  - `market_ret_1`
  - `close`
- Config settings:
  - `COST_BPS`
  - `LONG_ONLY`
  - thresholds
  - holding constraints
- `mode_profile.py` settings:
  - `up_th`
  - `down_th`
  - `min_hold`
  - `neutral_to_long`

## Outputs

- `outputs/backtest_metrics.json`
- `outputs/equity_curve.csv`
- `outputs/equity_curve.png`

## Signal to position logic

1) Map probability to raw signal:
- `+1` if `p >= up_th`
- `-1` if `p <= down_th`
- `0` otherwise

2) If `LONG_ONLY = True`:
- Conservative mode usually uses `{1, 0}`.
- Aggressive mode may map neutral to long.

3) Apply minimum hold bars with `_apply_min_hold` to reduce fast flipping.

4) Shift signal by one bar before applying returns:
- `position_t = signal_(t-1)`
- This avoids lookahead bias.

## Returns and costs

- Strategy return per bar:
  - `strat_ret = position * market_ret - cost`
- Turnover:
  - `turnover = abs(position_t - position_(t-1)) / 2`
- Trading cost:
  - `cost = turnover * (COST_BPS / 10000)`
- Buy-and-hold return:
  - `bh_ret = market_ret`

## Performance metrics

- Equity curve from cumulative product of `(1 + return)`.
- Reported metrics include:
  - `FinalEquity`
  - `CAGR`
  - annualized volatility
  - Sharpe
  - Sortino
  - Max Drawdown
  - average holding period (bars)

## Why this file matters

- Evaluation step says whether direction classification improved.
- Backtest step says whether that edge survives trading assumptions and costs.