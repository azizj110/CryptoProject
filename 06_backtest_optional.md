## 06_backtest_optional.py

This script converts model predictions into a trading simulation for the test period.

It is optional in the pipeline, but useful to check whether prediction quality becomes PnL.

## Inputs

- `outputs/predictions.csv`:
  - `y_pred`
  - optional `y_prob_up`
  - `market_ret_1`
  - `close`
- `config.py`:
  - `COST_BPS`
  - `LONG_ONLY`
  - thresholds
  - holding constraints
- `mode_profile.py`:
  - `up_th`
  - `down_th`
  - `min_hold`
  - `neutral_to_long`

## Outputs

- `outputs/backtest_metrics.json`
- `outputs/equity_curve.csv`
- `outputs/equity_curve.png`

## Signal-to-position logic

1) Convert probability to raw signal:
- `+1` if `p >= up_th`
- `-1` if `p <= down_th`
- `0` otherwise

2) If `LONG_ONLY = True`:
- conservative mode usually keeps `{1, 0}`
- aggressive mode may map neutral to long

3) Apply minimum hold using `_apply_min_hold` to reduce rapid flipping.

4) Shift by one bar before applying returns:
- `position_t = signal_(t-1)`
- this avoids lookahead bias

## Returns and cost model

- strategy return:
  - `strat_ret = position * market_ret - cost`
- turnover:
  - `turnover = abs(position_t - position_(t-1)) / 2`
- trading cost:
  - `cost = turnover * (COST_BPS / 10000)`
- buy-and-hold:
  - `bh_ret = market_ret`

## Performance metrics

From the equity curve (cumulative product of `1 + return`), we report:
- `FinalEquity`
- `CAGR`
- annualized volatility
- Sharpe
- Sortino
- Max Drawdown
- average holding period (bars)

## Why this matters

Evaluation shows classification quality.
Backtesting shows whether the edge survives costs and execution assumptions.