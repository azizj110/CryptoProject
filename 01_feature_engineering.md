## 01_feature_engineering.py

This file builds model input features from raw price data.

Output file:
- `processed/features.csv`

## Main logic

We create momentum, volatility, trend, serial-correlation, and regime features.

Main features:
- One-bar return: `ret_1 = close / close.shift(1) - 1`
- K-bar return: `ret_k = close / close.shift(k) - 1`
- Rolling volatility: rolling standard deviation of `ret_1` over a window `w`
- Moving average gap: `ma_gap = sma_fast / sma_slow - 1`
- Crossover flag: `ma_cross = 1` when `sma_fast > sma_slow`, else `0`
- Lag feature: `ret_lag1 = ret_1.shift(1)`

We also compute:
- RSI
- Optional `vol_spike` when aggressive mode is enabled

## Regime model

We try a 2-state Markov switching model on returns.

Saved outputs:
- `regime_prob_high_vol`
- `regime_state_high_vol`

If `statsmodels` is not available, we use a rolling-volatility rule as a fallback regime proxy.

## Notes

This file also keeps:
- `close`
- `market_ret_1`

These are used later for evaluation and backtesting.